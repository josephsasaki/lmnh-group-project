terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.89.0"
    }
  }
}

data "aws_vpc" "c16_vpc" {
  id = var.VPC_ID
}

data "aws_s3_bucket" "c16-trenet-athena-output-s3" {
  bucket = var.ATHENA_BUCKET_NAME
}

resource "aws_athena_database" "athena_db" {
  name   = var.ATHENA_DB_NAME  
  bucket = data.aws_s3_bucket.c16-trenet-athena-output-s3.id  
}

# resource "aws_iam_role" "athena_role" {
#   name = "athena-role"
  
#   assume_role_policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Action = "sts:AssumeRole",
#         Effect = "Allow",
#         Principal = {
#           Service = "athena.amazonaws.com"
#         }
#       }
#     ]
#   })
# }

# resource "aws_iam_role_policy" "athena_policy" {
#   name   = "athena-policy"
#   role   = aws_iam_role.athena_role.id
#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Action = [
#           "s3:GetObject",
#           "s3:ListBucket"
#         ],
#         Effect   = "Allow",
#         Resource = [
#           "arn:aws:s3:::c16-trenet-s3",
#           "arn:aws:s3:::c16-trenet-s3/*"
#         ]
#       },
#       {
#         Action = "athena:StartQueryExecution",
#         Effect = "Allow",
#         Resource = "*"
#       }
#     ]
#   })
# }
