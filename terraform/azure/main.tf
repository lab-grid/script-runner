terraform {
  required_providers {
    acme = {
      source = "vancluever/acme"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "acme" {
  server_url = "https://acme-staging-v02.api.letsencrypt.org/directory"
}

terraform {
  backend "azurerm" {
    resource_group_name  = "labgrid"
    storage_account_name = "labgridtfstate"
    container_name       = "swabseq-analysis-example-tfstate"
    key                  = "prod.terraform.tfstate"
  }
}


# Resource Group --------------------------------------------------------------

resource "azurerm_resource_group" "swabseq_analysis_example" {
  name     = "swabseq-analysis-example"
  location = var.location
}


# VPC/ECS ---------------------------------------------------------------------

resource "azurerm_virtual_network" "vnet" {
  name                = "${var.stack_name}-vnet"
  resource_group_name = azurerm_resource_group.swabseq_analysis_example.name
  location            = var.location
  address_space       = ["10.0.0.0/16"]
  tags                = var.tags
}

resource "azurerm_subnet" "redis_subnet" {
  name                 = var.redis_subnet_name
  resource_group_name  = azurerm_resource_group.swabseq_analysis_example.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "worker_subnet" {
  name                 = var.worker_subnet_name
  resource_group_name  = azurerm_resource_group.swabseq_analysis_example.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.3.0/24"]

  delegation {
    name = "${var.stack_name}-script-runner-worker-delegation"
    service_delegation {
      name    = "Microsoft.ContainerInstance/containerGroups"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "gateway_subnet" {
  name                 = var.gateway_subnet_name
  resource_group_name  = azurerm_resource_group.swabseq_analysis_example.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.4.0/24"]

  service_endpoints = ["Microsoft.KeyVault"]
}


# swabseq-analysis ------------------------------------------------------------

module "swabseq_analysis" {
  source = "github.com/lab-grid/terraform-azurerm-container-instances-script-runner"

  location            = var.location
  resource_group_name = azurerm_resource_group.swabseq_analysis_example.name

  redis_subnet_id  = azurerm_subnet.redis_subnet.id
  worker_subnet_id = azurerm_subnet.worker_subnet.id
  gateway_subnet_id = azurerm_subnet.gateway_subnet.id

  stack_name = var.stack_name

  auth_provider = "none"

  image     = "labflow/script-runner-example"
  image_tag = var.image_tag

  dns_subdomain                = var.dns_subdomain
  dns_zone_name                = var.dns_zone_name
  dns_zone_resource_group_name = var.dns_zone_resource_group_name
}
