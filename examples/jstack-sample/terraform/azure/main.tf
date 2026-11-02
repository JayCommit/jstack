variable "location" {
  type        = string
  description = "Azure region for the sample resource group and network."
  default     = "uksouth"

  validation {
    condition     = contains(["uksouth"], var.location)
    error_message = "location must be uksouth."
  }
}

variable "address_space" {
  type        = list(string)
  description = "Address space for the sample virtual network."
  default     = ["10.0.0.0/16"]
}

resource "azurerm_resource_group" "this" {
  name     = "rg-example"
  location = var.location
}

resource "azurerm_virtual_network" "this" {
  name                = "vnet-example"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  address_space       = var.address_space
}

resource "azurerm_subnet" "app" {
  name                 = "snet-app"
  resource_group_name  = azurerm_resource_group.this.name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_security_group" "app" {
  name                = "nsg-app"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
}

resource "azurerm_subnet_network_security_group_association" "app" {
  subnet_id                 = azurerm_subnet.app.id
  network_security_group_id = azurerm_network_security_group.app.id
}
