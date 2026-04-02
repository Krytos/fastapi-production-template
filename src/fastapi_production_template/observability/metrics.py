"""Simple in-memory Prometheus-like metrics store."""

from dataclasses import dataclass, field
from threading import Lock


@dataclass(kw_only=True)
class RequestStats:
    """Aggregated stats for a method/path/status tuple."""

    count: int = 0
    total_duration_seconds: float = 0.0


@dataclass(kw_only=True)
class MetricsStore:
    """Track request count, latency, and in-flight requests."""

    in_flight: int = 0
    requests: dict[tuple[str, str, int], RequestStats] = field(default_factory=dict)
    _lock: Lock = field(default_factory=Lock)

    def increment_in_flight(self) -> None:
        with self._lock:
            self.in_flight += 1

    def decrement_in_flight(self) -> None:
        with self._lock:
            self.in_flight -= 1

    def observe(self, *, method: str, path: str, status_code: int, duration_seconds: float) -> None:
        key = (method, path, status_code)
        with self._lock:
            stats = self.requests.setdefault(key, RequestStats())
            stats.count += 1
            stats.total_duration_seconds += duration_seconds

    def render(self) -> str:
        lines: list[str] = [
            "# HELP http_requests_total Total HTTP requests",
            "# TYPE http_requests_total counter",
        ]
        with self._lock:
            for (method, path, status), stats in sorted(self.requests.items()):
                lines.append(f'http_requests_total{{method="{method}",path="{path}",status="{status}"}} {stats.count}')
            lines.extend(
                [
                    "# HELP http_request_duration_seconds_total Cumulative HTTP request duration in seconds",
                    "# TYPE http_request_duration_seconds_total counter",
                ]
            )
            for (method, path, status), stats in sorted(self.requests.items()):
                lines.append(
                    "http_request_duration_seconds_total"
                    f'{{method="{method}",path="{path}",status="{status}"}} '
                    f"{stats.total_duration_seconds:.6f}"
                )
            lines.extend(
                [
                    "# HELP http_requests_in_flight Current in-flight HTTP requests",
                    "# TYPE http_requests_in_flight gauge",
                    f"http_requests_in_flight {self.in_flight}",
                ]
            )
        return "\n".join(lines) + "\n"
