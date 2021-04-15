variable "location" {
  type    = string
  default = "westus"
}

variable "stack_name" {
  type    = string
  default = "swabseq-analysis-example"
}

variable "image_tag" {
  type    = string
  default = "latest"
}

variable "dns_subdomain" {
  type        = string
  description = "Subdomain to prefix to dns_zone_name. API will be served under this subdomain."
}

variable "dns_zone_name" {
  type        = string
  description = "Identifier of the Route53 Hosted Zone for this instance of script-runner."
}

variable "redis_subnet_name" {
  type        = string
  default     = "redis-subnet"
  description = "Name of the redis subnet that will be created."
}

variable "server_subnet_name" {
  type        = string
  default     = "server-subnet"
  description = "Name of the server subnet that will be created."
}

variable "worker_subnet_name" {
  type        = string
  default     = "worker-subnet"
  description = "Name of the worker subnet that will be created."
}

variable "tags" {
  type = map(string)

  default = {
    Terraform   = "true"
    Environment = "dev"
  }
}
