variable "DB_USERNAME" {
  description = "The username to connect to the rds"
  type = string
}

variable "DB_PASSWORD" {
  description = "The password to connect to the rds"
  type = string
}

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

variable "SG_NAME" {
  description = "Name of the security group the rds will be in"
  type = string
  default = "c16-trenet-sg"
}

variable "RDS_NAME" {
  description = "The name of the rds"
  type = string
  default = "c16-trenet-sql-serv-rds"
}

variable "RDS_SUBNET_GROUP_NAME" {
  description = "The name of the subnet group"
  type = string
  default = "c16-public-subnet-group"
}

