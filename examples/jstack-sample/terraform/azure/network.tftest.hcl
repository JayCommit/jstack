mock_provider "azurerm" {}

run "plan_network" {
  command = plan

  variables {
    location = "uksouth"
  }

  assert {
    condition     = azurerm_resource_group.this.location == "uksouth"
    error_message = "Resource group location must be uksouth."
  }

  assert {
    condition     = contains(azurerm_virtual_network.this.address_space, "10.0.0.0/16")
    error_message = "Virtual network address space must include 10.0.0.0/16."
  }

  assert {
    condition     = contains(azurerm_subnet.app.address_prefixes, "10.0.1.0/24")
    error_message = "Application subnet prefixes must include 10.0.1.0/24."
  }
}
