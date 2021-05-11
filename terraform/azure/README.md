# script-runner Azure Example

This stack deploys the script-runner [example](https://github.com/lab-grid/script-runner/blob/main/docker/Dockerfile.example)

```sh
# From the terraform/azure directory:
terraform init
terraform apply
```

NOTE: After deploying, you must go to your azure portal and find the redis cache that was created. Navigate
to the private-endpoints section and enable public network access. This currently does not get enabled
properly by the azurerm terraform provider.

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_swabseq_analysis"></a> [swabseq\_analysis](#module\_swabseq\_analysis) | github.com/lab-grid/terraform-azurerm-container-instances-script-runner |  |

## Resources

| Name | Type |
|------|------|
| [azurerm_resource_group.swabseq_analysis_example](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group) | resource |
| [azurerm_subnet.gateway_subnet](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet) | resource |
| [azurerm_subnet.redis_subnet](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet) | resource |
| [azurerm_subnet.worker_subnet](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet) | resource |
| [azurerm_virtual_network.vnet](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_dns_subdomain"></a> [dns\_subdomain](#input\_dns\_subdomain) | Subdomain to prefix to dns\_zone\_name. API will be served under this subdomain. | `string` | n/a | yes |
| <a name="input_dns_zone_name"></a> [dns\_zone\_name](#input\_dns\_zone\_name) | Identifier of the Route53 Hosted Zone for this instance of script-runner. | `string` | n/a | yes |
| <a name="input_dns_zone_resource_group_name"></a> [dns\_zone\_resource\_group\_name](#input\_dns\_zone\_resource\_group\_name) | Name of the resource group dns\_zone\_name is in. | `string` | n/a | yes |
| <a name="input_gateway_subnet_name"></a> [gateway\_subnet\_name](#input\_gateway\_subnet\_name) | Name of the subnet to create application gateway instances in. | `string` | `"gateway-subnet"` | no |
| <a name="input_image_tag"></a> [image\_tag](#input\_image\_tag) | n/a | `string` | `"latest"` | no |
| <a name="input_location"></a> [location](#input\_location) | n/a | `string` | `"westus"` | no |
| <a name="input_redis_subnet_name"></a> [redis\_subnet\_name](#input\_redis\_subnet\_name) | Name of the redis subnet that will be created. | `string` | `"redis-subnet"` | no |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | n/a | `string` | `"script-runner-example"` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | n/a | `map(string)` | <pre>{<br>  "Environment": "dev",<br>  "Terraform": "true"<br>}</pre> | no |
| <a name="input_worker_subnet_name"></a> [worker\_subnet\_name](#input\_worker\_subnet\_name) | Name of the worker subnet that will be created. | `string` | `"worker-subnet"` | no |

## Outputs

No outputs.
