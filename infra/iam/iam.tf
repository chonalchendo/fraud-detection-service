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

variable "user_arn" {
  type = list(string)
  description = "IAM users allowed to access the bucket"
}

data "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
}

resource "aws_iam_user" "user" {
  name = var.name
  tags = var.tags
}

resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = data.aws_s3_bucket.bucket.id
  policy = data.aws_iam_policy_document.bucket_policy.json
}

data "aws_iam_policy_document" "bucket_policy" {
  statement {
    principals {
      type        = "AWS"
      identifiers = var.user_arn
    }
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket"
    ]
    resources = [
      var.bucket_arn,
      "${var.bucket_arn}/*"
    ]
  }
}


# resource "aws_iam_access_key" "access_key" {
#   user = aws_iam_user.user.name
# }
#
# output "access_key" {
#   value = aws_iam_access_key.access
# }
