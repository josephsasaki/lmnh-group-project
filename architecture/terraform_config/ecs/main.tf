terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.89.0"
    }
  }
}

provider "aws" {
  region = var.REGION
}

data "aws_vpc" "c16_vpc" {
  id = var.VPC_ID
}

resource "aws_ecs_service_definition" "c16-trenet-service-ecs" {
  family                   = var.ECS_SERVICE
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]  # Adjust based on your ECS launch type
  cpu                      = 512  # 0.5 vCPU at the task level
  memory                   = 1024
  execution_role_arn = var.execution_role_arn
  container_definitions = jsonencode([
    {
      name      = var.DASHBOARD_ECR
      image     = var.DASHBOARD_ECR_IMAGE 
      cpu       = 512  # 0.5 vCPU (AWS ECS uses 1024 CPU units = 1 vCPU)
      memory    = 1024  # 1GB RAM
      essential = true
      portMappings = [
        {
          containerPort = 8501
          hostPort      = 8501
          protocol      = "tcp"
        }
      ]
       environment = [
        { name = "AWS_ACCESS_KEY", value = var.AWS_ACCESS_KEY },
        { name = "AWS_SECRET_KEY", value = var.AWS_SECRET_KEY },
        { name = "DB_HOST", value = var.DB_HOST },
        { name = "DB_PORT", value = var.DB_PORT },
        { name = "DB_NAME", value = var.DB_NAME },
        { name = "DB_USER", value = var.DB_USERNAME },
        { name = "DB_PASSWORD", value = var.DB_PASSWORD }

      ]
    }
  ]) 
  }
  