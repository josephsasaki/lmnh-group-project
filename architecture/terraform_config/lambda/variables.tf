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

variable "PIPELINE1_ECR" {
  description = "Name of the ecr for pipeline 1"
  type = string
  default = "c16-trenet-pipeline1-ecr"
}

variable "PIPELINE2_ECR" {
  description = "Name of the ecr for pipeline 2"
  type = string
  default = "c16-trenet-pipeline2-ecr"
}

variable "LAMBDA_NAME1" {
  description = "The name of the lambda function for pipeline 1"
  type = string
  default = "c16-trenet-pipeline1-lambda"
}

variable "LAMBDA_NAME2" {
  description = "The name of the lambda function for pipeline 2"
  type = string
  default = "c16-trenet-pipeline2-lambda"
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


