variable "azure_location" {
  description = "Azure region for infrastructure"
  type        = string
  default     = "westeurope"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "fastapi-production-template"
}

variable "resource_group_name" {
  description = "Resource group name for shared resources"
  type        = string
  default     = "fastapi-production-template-rg"
}

variable "container_registry_name" {
  description = "Globally unique Azure Container Registry name (5-50 alphanumeric lowercase)"
  type        = string
  default     = "fastapiprodtemplateacr"
}
