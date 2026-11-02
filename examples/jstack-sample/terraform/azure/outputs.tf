output "resource_group_name" {
  description = "Name of the sample resource group."
  value       = azurerm_resource_group.this.name
}

output "subnet_id" {
  description = "Resource id of the sample application subnet."
  value       = azurerm_subnet.app.id
}
