resource "aws_s3_bucket" "c16_trenet_s3" {
  bucket = "c16-trenet-s3"

  tags = {
    Name = "c16-trenet-s3"
  }
}

# Enable Versioning
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.c16_trenet_s3.id
  versioning_configuration {
    status = "Enabled"
  }
}
