resource "aws_ecr_repository" "c16-trenet-pipeline1-ecr" {
  name                 = var.PIPELINE1_ECR
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "c16-trenet-pipeline2-ecr" {
  name                 = var.PIPELINE2_ECR
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "c16-trenet-dashboard-ecr" {
  name                 = var.DASHBOARD_ECR
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}