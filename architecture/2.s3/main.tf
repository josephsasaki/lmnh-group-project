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


resource "aws_s3_bucket" "c16_trenet_s3" {
  bucket = var.BUCKET_NAME

  tags = {
    Name = var.BUCKET_NAME
  }
}

# Enable Versioning
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.c16_trenet_s3.id
  versioning_configuration {
    status = "Enabled"
  }
}


resource "aws_s3_bucket" "c16-trenet-athena-output-s3" {
  bucket = var.BUCKET_NAME2

  tags = {
    Name = var.BUCKET_NAME2
  }
}