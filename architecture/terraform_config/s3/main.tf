resource "aws_s3_bucket" "c16_trenet_s3" {
  bucket = var.BUCKET_NAME

  tags = {
    Name = var.BUCKET_NAME
  }
}

# Enable Versioning
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.c16_trenet_s3.id
  versioning_configuration {
    status = "Enabled"
  }
}
