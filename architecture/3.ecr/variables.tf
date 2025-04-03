
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

variable "DASHBOARD_ECR" {
  description = "Name of the ecr for the dashboard"
  type = string
  default = "c16-trenet-dashboard-ecr"
}



