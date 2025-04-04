terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.89.0"
    }
  }
}

data "aws_s3_bucket" "c16-trenet-athena-output-s3" {
  bucket = var.ATHENA_BUCKET_NAME
}

resource "aws_athena_database" "athena_db" {
  name   = var.ATHENA_DB_NAME  
  bucket = data.aws_s3_bucket.c16-trenet-athena-output-s3.id  
}