variable "ATHENA_BUCKET_NAME" {
  description = "Name of the s3 athena queries bucket"
  type = string
  default = "c16-trenet-athena-output-s3"
}

variable "ATHENA_DB_NAME" {
  description = "Name of the athena database"
  type = string
  default = "c16_trenet_athena_query_db"
}

