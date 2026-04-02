terraform {
  required_version = ">= 1.8.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.30"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_artifact_registry_repository" "api" {
  location      = var.gcp_region
  repository_id = var.artifact_registry_repository_id
  description   = "Docker repository for API images"
  format        = "DOCKER"
}
