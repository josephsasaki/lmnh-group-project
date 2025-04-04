terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
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

resource "aws_security_group" "c16-trenet-ecs-sg" {
  name        = var.SG_NAME
  description = "Sg for sql server rds"
  vpc_id      = data.aws_vpc.c16_vpc.id

  ingress {
    from_port        = 1433
    to_port          = 8502
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = -1
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  tags = {
    Name = var.SG_NAME
  }
}

resource "aws_ecs_task_definition" "c16-trenet-task" {
  family                   = var.ECS_TASK_DEF
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = var.EXECUTION_ROLE_ARN

  container_definitions = jsonencode([
    {
      name      = var.DASHBOARD_ECR
      image     = var.DASHBOARD_ECR_IMAGE
      cpu       = 512
      memory    = 1024
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
        { name = "DB_USERNAME", value = var.DB_USERNAME },
        { name = "DB_PASSWORD", value = var.DB_PASSWORD }
      ]
    }
  ])
}

resource "aws_ecs_service" "c16-trenet-service-ecs" {
  name            = var.ECS_SERVICE
  cluster         = var.ECS_CLUSTER
  task_definition = aws_ecs_task_definition.c16-trenet-task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [var.SUBNET1, var.SUBNET2, var.SUBNET3]
    security_groups  = [aws_security_group.c16-trenet-ecs-sg.id]
    assign_public_ip = true
  }
}
