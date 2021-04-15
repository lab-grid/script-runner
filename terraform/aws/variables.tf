variable "aws_region" {
  type    = string
  default = "us-west-1"
}

variable "stack_name" {
  type    = string
  default = "swabseq-analysis-example"
}

variable "dns_subdomain" {
  type = string
}

variable "dns_zone_id" {
  type = string
}

variable "image_tag" {
  type    = string
  default = "latest"
}
