variable "aws_region" {
  type    = string
  default = "us-west-1"
}

variable "stack_name" {
  type    = string
  default = "swabseq-analysis-example"
}

variable "dns_name" {
  type = string
}

variable "dns_zone_id" {
  type = string
}

variable "auth0_domain" {
  type = string
}

variable "auth0_audience" {
  type = string
}

variable "auth0_client_id" {
  type = string
}

variable "image_tag" {
  type    = string
  default = "latest"
}

variable "dns_subdomain" {
  type = string
}

variable "dns_domain" {
  type        = string
  description = "DNS name for this instance of script-runner. Must match 'dns_zone_id'."
}

variable "dns_zone_name" {
  type        = string
  description = "Identifier of the Route53 Hosted Zone for this instance of script-runner."
}

variable "redis_subnet_name" {
  type = string
  default = "redis-subnet"
}

variable "server_subnet_name" {
  type = string
  default = "server-subnet"
}

variable "worker_subnet_name" {
  type = string
  default = "worker-subnet"
}

variable "tags" {
  type = map(string)
  default = {
    Terraform   = "true"
    Environment = "dev"
  }
}
