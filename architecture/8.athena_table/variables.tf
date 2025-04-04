
variable "ATHENA_DB_NAME" {
  description = "Name of the athena database"
  type = string
  default = "c16_trenet_athena_query_db"
}

variable "ATHENA_TABLE_NAME" {
  description = "Name of the athena TABLE"
  type = string
  default = "c16_trenet_athena_table"
}


variable "BUCKET_LOCATION" {
  description = "Location of the s3 archive bucket"
  type = string
  default = "s3://c16-trenet-s3/"
}



