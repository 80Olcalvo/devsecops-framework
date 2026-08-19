terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  type        = string
  description = "ID del proyecto en Google Cloud Platform"
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "Región de GCP para el despliegue de recursos"
}

variable "environment" {
  type        = string
  description = "Ambiente de ejecución (qa o prod)"
}

variable "service_name" {
  type        = string
  default     = "secure-api"
  description = "Nombre del microservicio"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# -----------------------------------------------------------------------------
# Artifact Registry Repository
# -----------------------------------------------------------------------------
resource "google_artifact_registry_repository" "app_repo" {
  location      = var.region
  repository_id = "devsecops-apps"
  description   = "Repositorio Docker para microservicios DevSecOps (${var.environment})"
  format        = "DOCKER"
}

# -----------------------------------------------------------------------------
# Cloud Run Service
# -----------------------------------------------------------------------------
resource "google_cloud_run_v2_service" "app_service" {
  name     = "${var.service_name}-${var.environment}"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.app_repo.repository_id}/app:latest"
      
      resources {
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
        }
      }

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }

      ports {
        container_port = 8000
      }

      startup_probe {
        http_get {
          path = "/healthz"
          port = 8000
        }
        initial_delay_seconds = 5
        period_seconds        = 10
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/healthz"
          port = 8000
        }
        period_seconds    = 15
        failure_threshold = 3
      }
    }
  }
}

# Permitir invocación no autenticada para API pública
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = google_cloud_run_v2_service.app_service.project
  location = google_cloud_run_v2_service.app_service.location
  name     = google_cloud_run_v2_service.app_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "service_url" {
  description = "URL pública del servicio Cloud Run"
  value       = google_cloud_run_v2_service.app_service.uri
}
