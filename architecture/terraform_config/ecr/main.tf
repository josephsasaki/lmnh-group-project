resource "aws_ecr_repository" "c16-trenet-pipeline1-ecr" {
  name                 = "c16-trenet-pipeline1-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "c16-trenet-pipeline2-ecr" {
  name                 = "c16-trenet-pipeline2-ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}