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

resource "aws_security_group" "c16-trenet-sg" {
  name        = var.SG_NAME
  description = "Sg for sql server rds"
  vpc_id      = data.aws_vpc.c16_vpc.id

  ingress {
    from_port        = 1433
    to_port          = 1433
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


resource "aws_db_instance" "c16-trenet-rds" {
  allocated_storage            = 20
  identifier                   = var.RDS_NAME
  engine                       = "sqlserver-ex"
  engine_version               = "16.00.4175.1.v1"
  instance_class               = "db.t3.micro"
  publicly_accessible          = true
  performance_insights_enabled = false
  skip_final_snapshot          = true
  db_subnet_group_name         = var.RDS_SUBNET_GROUP_NAME
  vpc_security_group_ids       = [aws_security_group.c16-trenet-sg.id]
  username                     = var.DB_USERNAME
  password                     = var.DB_PASSWORD
}