output "azure_location" {
  description = "Configured Azure location"
  value       = var.azure_location
}

output "resource_group_name" {
  description = "Resource group where resources are created"
  value       = azurerm_resource_group.main.name
}

output "container_registry_name" {
  description = "Azure Container Registry name"
  value       = azurerm_container_registry.api.name
}

output "container_registry_login_server" {
  description = "Azure Container Registry login server"
  value       = azurerm_container_registry.api.login_server
}
