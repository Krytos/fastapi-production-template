from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TERRAFORM_DIRS = (
    "infra/terraform-aws",
    "infra/terraform-azure",
    "infra/terraform-gcp",
)


def run_terraform_fmt_check(directory: str) -> None:
    subprocess.run(
        ["terraform", f"-chdir={ROOT / directory}", "fmt", "-check"],
        check=True,
    )


def main() -> int:
    for directory in TERRAFORM_DIRS:
        print(f"Running terraform fmt -check in {directory}")
        run_terraform_fmt_check(directory)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"terraform fmt check failed with exit code {exc.returncode}", file=sys.stderr)
        raise SystemExit(exc.returncode) from exc
