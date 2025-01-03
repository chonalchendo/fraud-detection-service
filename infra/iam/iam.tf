variable "name" {
  type = string
}

variable "tags" {
  type = map
  description = "Project tags"
}

variable "bucket_name" {
  type = string
}

variable "bucket_arn" {
  type = string
}

data "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
}

resource "aws_iam_user" "user" {
  name = var.name
  tags = var.tags
}


