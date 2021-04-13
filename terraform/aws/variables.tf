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
