output "gcp_project_id" {
  description = "Configured GCP project id"
  value       = var.gcp_project_id
}

output "gcp_region" {
  description = "Configured GCP region"
  value       = var.gcp_region
}

output "artifact_registry_repository_id" {
  description = "Artifact Registry repository id"
  value       = google_artifact_registry_repository.api.repository_id
}

output "artifact_registry_repository_url" {
  description = "Docker Artifact Registry repository path"
  value       = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.api.repository_id}"
}
