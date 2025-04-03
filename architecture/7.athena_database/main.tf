terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.89.0"
    }
  }
}


# Create an S3 bucket for storing Athena query results
resource "aws_s3_bucket" "c16trenetqueries" {
  bucket = "c16-trenet-queries" # Replace with your desired bucket name
}

# Create an Athena database
resource "aws_athena_database" "example" {
  name   = "c16_trenet_query_db"  # Replace with your desired database name
  bucket = aws_s3_bucket.c16trenetqueries.id  # S3 bucket to store query results
}


# Add necessary IAM role and policy for Athena (if not already created)
resource "aws_iam_role" "athena_role" {
  name = "athena-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "athena.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "athena_policy" {
  name   = "athena-policy"
  role   = aws_iam_role.athena_role.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Effect   = "Allow",
        Resource = [
          "arn:aws:s3:::c16-trenet-s3",
          "arn:aws:s3:::c16-trenet-s3/*"
        ]
      },
      {
        Action = "athena:StartQueryExecution",
        Effect = "Allow",
        Resource = "*"
      }
    ]
  })
}
