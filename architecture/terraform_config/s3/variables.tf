variable "BUCKET_NAME" {
  description = "Name of the s3 bucket"
  type = string
  default = "c16-trenet-s3"
}

variable "REGION" {
  description = "Desired region the s3 will be in"
  type = string
  default = "eu-west-2"
}
