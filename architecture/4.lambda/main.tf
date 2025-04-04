provider "aws" {
    region = var.BUCKET_REGION
    secret_key = var.SECRET_ACCESS_KEY_ID
    access_key = var.ACCESS_KEY_ID
}

## ECR

data "aws_ecr_repository" "c16-trenet-pipeline" {
  name = var.PIPELINE1_ECR
}

data "aws_ecr_image" "lambda-image-pipeline" {
  repository_name = data.aws_ecr_repository.c16-trenet-pipeline.name
  image_tag       = "latest"
}

data "aws_ecr_repository" "c16-trenet-pipeline2" {
  name = var.PIPELINE2_ECR
}

data "aws_ecr_image" "lambda-image-pipeline2" {
  repository_name = data.aws_ecr_repository.c16-trenet-pipeline2.name
  image_tag       = "latest"
}

## Permissions etc. for the Lambda

# Trust doc
data "aws_iam_policy_document" "lambda-role-trust-policy-doc" {
    statement {
      effect = "Allow"
      principals {
        type = "Service"
        identifiers = [ "lambda.amazonaws.com" ]
      }
      actions = [
        "sts:AssumeRole"
      ]
    }
}

# Permissions doc
data "aws_iam_policy_document" "lambda-role-permissions-policy-doc" {
    statement {
      effect = "Allow"
      actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      resources = [ "arn:aws:logs:eu-west-2:129033205317:*" ]
    }
}

# Role
resource "aws_iam_role" "lambda-role" {
    name = "c16-tenet-lambda-pipelines-role"
    assume_role_policy = data.aws_iam_policy_document.lambda-role-trust-policy-doc.json
}

# Permissions policy
resource "aws_iam_policy" "lambda-role-permissions-policy" {
    name = "c16-trenet-lambda-pipelines-permissions-policy"
    policy = data.aws_iam_policy_document.lambda-role-permissions-policy-doc.json
}

# Connect the policy to the role
resource "aws_iam_role_policy_attachment" "lambda-role-policy-connection" {
  role = aws_iam_role.lambda-role.name
  policy_arn = aws_iam_policy.lambda-role-permissions-policy.arn
}

## Lambda
resource "aws_lambda_function" "c16-trenet-lambda-pipeline1" {
  function_name = var.LAMBDA_NAME1
  role = aws_iam_role.lambda-role.arn
  package_type = "Image"
  image_uri = data.aws_ecr_image.lambda-image-pipeline.image_uri
  timeout = 120
  environment {
    variables = {
         DB_USERNAME = var.DB_USERNAME
         DB_PASSWORD = var.DB_PASSWORD
         DB_PORT = var.DB_PORT
         DB_NAME = var.DB_NAME
         DB_DRIVER = var.DB_DRIVER
         DB_HOST = var.DB_HOST
    }
  }
}

## Lambda
resource "aws_lambda_function" "c16-trenet-lambda-pipeline2" {
  function_name = var.LAMBDA_NAME2
  role = aws_iam_role.lambda-role.arn
  package_type = "Image"
  image_uri = data.aws_ecr_image.lambda-image-pipeline2.image_uri
  timeout = 120
  environment {
    variables = {
         DB_USERNAME = var.DB_USERNAME
         DB_PASSWORD = var.DB_PASSWORD
         DB_PORT = var.DB_PORT
         DB_NAME = var.DB_NAME
         DB_DRIVER = var.DB_DRIVER
         DB_HOST = var.DB_HOST
         BUCKET_REGION = var.BUCKET_REGION
         S3_BUCKET = var.S3_BUCKET
         ACCESS_KEY_ID = var.ACCESS_KEY_ID
         SECRET_ACCESS_KEY_ID = var.SECRET_ACCESS_KEY_ID



    }
  }
}