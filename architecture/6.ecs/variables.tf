variable "REGION" {
  description = "Desired region the lambdas are located in"
  type = string
  default = "eu-west-2"
}

variable "VPC_ID" {
  description = "The vpc the lambda will be located on"
  type = string
  default = "vpc-0f7ba8057a52dd82d"
}

variable "DB_PORT" {
  description = "The port number to connect to the rds"
  type = string
  default = "1433"
}

variable "DB_DRIVER" {
  description = "The driver to connect to the database"
  type = string
  default = "ODBC Driver 18 for SQL Server"
}

variable "DB_USERNAME" {
  description = "The username to connect to the rds"
  type = string
}

variable "DB_PASSWORD" {
  description = "The password to connect to the rds"
  type = string
}

variable "DB_NAME" {
  description = "The SQL server database name"
  type = string
}

variable "AWS_SECRET_KEY" {
  description = "The users AWS secret key"
  type = string
}

variable "AWS_ACCESS_KEY" {
  description = "The users AWS access key"
  type = string
}


variable "DB_HOST" {
  description = "The RDS end point"
  type = string
}

variable "DASHBOARD_ECR" {
  description = "Name of the ecr for the dashboard"
  type = string
  default = "c16-trenet-dashboard-ecr"
}

variable "DASHBOARD_ECR_IMAGE" {
  description = "Name of the ecr for the dashboard"
  type = string
}

variable "ECS_TASK_DEF" {
  description = "Name of the ecs task"
  type = string
  default = "c16-trenet-task-def-ecs"
}

variable "ECS_SERVICE" {
  description = "Name of the ecs service"
  type = string
  default = "c16-trenet-service-ecs"
}

variable "ECS_CLUSTER" {
  description = "Name of the ecs cluster"
  type = string
  default = "c16-ecs-cluster"
}

variable "SUBNET1" {
  description = "ID for subnet 1"
  type = string
}

variable "SUBNET2" {
  description = "ID for subnet 2"
  type = string
}

variable "SUBNET3" {
  description = "ID for subnet 3"
  type = string
}

variable "SG_NAME" {
  description = "SG NAME for ecs"
  type = string
  default = "c16-trenet-ecs-sg"
}

variable "EXECUTION_ROLE_ARN" {
  description = "Execution role for task def"
  type = string
  default = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"
}
