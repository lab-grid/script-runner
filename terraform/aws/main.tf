provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "labflow-tf-backend"
    key    = "swabseq-analysis-example-tf"
    region = "us-west-1"
  }
}


# IAM -------------------------------------------------------------------------

resource "aws_iam_role" "labflow_role" {
  name = "${input.stack_name}-role"

  # May be necessary: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role
  # force_detach_policies = true

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}


# VPC/ECS ---------------------------------------------------------------------

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${input.stack_name}-vpc"

  enable_nat_gateway   = true
  enable_dns_hostnames = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

module "ecs" {
  source = "terraform-aws-modules/ecs/aws"

  name = "${input.stack_name}-ecs"

  container_insights = true

  capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  default_capacity_provider_strategy = [
    {
      capacity_provider = "FARGATE_SPOT"
      weight = 1
    }
  ]

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}


# swabseq-analysis ------------------------------------------------------------

module "swabseq_analysis" {
  source = "github.com/lab-grid/terraform-aws-ecs-script-runner"

  aws_region = var.aws_region

  stack_name = var.stack_name

  auth_provider = "none"

  ecs_task_execution_role_arn  = aws_iam_role.labflow_role.arn
  ecs_task_execution_role_name = aws_iam_role.labflow_role.name
  ecs_cluster_id               = module.ecs.this_ecs_cluster_id

  vpc_id                  = module.vpc.vpc_id
  vpc_cidr                = module.vpc.vpc_cidr_block
  vpc_public_subnet_ids   = module.vpc.public_subnets
  vpc_database_subnet_ids = module.vpc.database_subnets

  image     = "labflow/swabseq-analysis-server-example"
  image_tag = var.image_tag

  dns_subdomain = var.dns_subdomain
  dns_zone_id   = var.dns_zone_id
}
