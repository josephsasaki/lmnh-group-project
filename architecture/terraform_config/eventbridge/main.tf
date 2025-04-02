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

# Reference the existing Lambda function (if it's already created)
data "aws_lambda_function" "existing_lambda" {
  function_name = var.LAMBDA_NAME1
}


# Reference the existing Lambda function (if it's already created)
data "aws_lambda_function" "existing_lambda2" {
  function_name = var.LAMBDA_NAME2
}

# Create the EventBridge Scheduler to trigger Lambda on a schedule with a flexible time window
resource "aws_scheduler_schedule" "scheduled_event" {
  name                = var.PIPELINE1_SCHEDULE_NAME
  description         = "Triggers Lambda function on a scheduled basis with a flexible time window"
  schedule_expression = var.SCHEDULE1_TRIGGER_RATE
  schedule_expression_timezone = "Europe/London"
  flexible_time_window {
    mode = "OFF"  
  }

  target {
    arn     = data.aws_lambda_function.existing_lambda.arn
    role_arn = aws_iam_role.scheduler_role.arn
    input = "{}" 

    retry_policy {
      maximum_retry_attempts       = 0  
    }
  }
}

# Create the EventBridge Scheduler to trigger Lambda on a schedule with a flexible time window
resource "aws_scheduler_schedule" "scheduled_event2" {
  name                = var.PIPELINE2_SCHEDULE_NAME
  description         = "Triggers Lambda function on a scheduled basis with a flexible time window"
  schedule_expression = var.SCHEDULE2_TRIGGER_RATE
  schedule_expression_timezone = "Europe/London"
  flexible_time_window {
    mode = "OFF"  
  }

  target {
    arn     = data.aws_lambda_function.existing_lambda2.arn
    role_arn = aws_iam_role.scheduler_role.arn
    input = "{}" 

    retry_policy {
      maximum_retry_attempts       = 0  
    }
  }
}

# IAM role for the scheduler to invoke the Lambda function
resource "aws_iam_role" "scheduler_role" {
  name = "eventbridge_scheduler_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}


# Grant the role permission to invoke the Lambda function
resource "aws_iam_policy" "scheduler_lambda_permission" {
  name        = "scheduler_lambda_invoke_policy"
  description = "Allows EventBridge Scheduler to invoke Lambda function"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action  = "lambda:InvokeFunction"
        Resource = data.aws_lambda_function.existing_lambda.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "scheduler_lambda_attach" {
  policy_arn = aws_iam_policy.scheduler_lambda_permission.arn
  role       = aws_iam_role.scheduler_role.name
}
