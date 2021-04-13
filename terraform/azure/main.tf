provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name  = "swabseq-analysis-example-rg"
    storage_account_name = "swabseq-analysis-example-tf"
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

module "vnet" {
  source              = "Azure/vnet/azurerm"
  resource_group_name = azurerm_resource_group.swabseq_analysis_example.name
  address_space       = ["10.0.0.0/16"]
  subnet_prefixes     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  subnet_names        = [var.redis_subnet_name, var.server_subnet_name, var.worker_subnet_name]

  # subnet_service_endpoints = {
  #   subnet2 = ["Microsoft.Storage", "Microsoft.Sql"],
  #   subnet3 = ["Microsoft.AzureActiveDirectory"]
  # }

  tags = var.tags

  depends_on = [azurerm_resource_group.example]
}


# swabseq-analysis ------------------------------------------------------------

module "swabseq_analysis" {
  source = "github.com/lab-grid/terraform-azurerm-container-instances-script-runner"

  region              = var.region
  location            = var.location
  resource_group_name = azurerm_resource_group.swabseq_analysis_example.name

  redis_subnet_id  = module.vnet.vnet_subnets[0]
  server_subnet_id = module.vnet.vnet_subnets[1]
  worker_subnet_id = module.vnet.vnet_subnets[2]

  stack_name = var.stack_name

  auth0_domain    = var.auth0_domain
  auth0_audience  = var.auth0_audience
  auth0_client_id = var.auth0_client_id

  image     = "labflow/swabseq-analysis-server-example"
  image_tag = var.image_tag

  dns_subdomain = var.dns_subdomain
  dns_domain    = var.dns_domain
  dns_zone_name = var.dns_zone_name
}
