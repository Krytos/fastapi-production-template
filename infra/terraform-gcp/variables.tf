variable "gcp_project_id" {
  description = "GCP project id for infrastructure resources"
  type        = string
}

variable "gcp_region" {
  description = "GCP region for infrastructure"
  type        = string
  default     = "europe-west3"
}

variable "project_name" {
  description = "Project name used for metadata and naming"
  type        = string
  default     = "fastapi-production-template"
}

variable "artifact_registry_repository_id" {
  description = "Artifact Registry repository id"
  type        = string
  default     = "fastapi-production-template-api"
}
