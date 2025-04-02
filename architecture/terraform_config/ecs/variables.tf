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

variable "ECS_SERVICE" {
  description = "Name of the ecs service"
  type = string
  default = "c16-trenet-service-ecs"
}

variable "DB_PORT" {
  description = "The port number to connect to the rds"
  type = number
  default = 1433
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
  default = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c16-trenet-dashboard-ecr"
}
