variable "user_name" {
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

variable "codeartifact_domain" {
  type = string
}

variable "codeartifact_repository" {
  type = string
}

variable "codeartifact_domain_arn" {
  type = string
}

variable "codeartifact_repo_arn" {
  type = string
}

data "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
}


resource "aws_iam_user" "user" {
  name = var.user_name
  tags = var.tags
}

resource "aws_iam_user_policy_attachment" "sts_user_policy_attachment" {
  user       = aws_iam_user.user.name
  policy_arn = aws_iam_policy.sts_user_policy.arn
}

resource "aws_iam_policy" "sts_user_policy" {
  name        = "AllowGetServiceBearerTokenForCodeArtifact"
  description = "Policy to allow sts:GetServiceBearerToken for CodeArtifact access"
  
  policy = data.aws_iam_policy_document.sts_user_policy_doc.json
}

data "aws_iam_policy_document" "sts_user_policy_doc" {
  statement {
    actions = [
      "sts:GetServiceBearerToken",
      "codeartifact:PublishPackageVersion"
    ]
    resources = ["*"]
  }
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

resource "aws_codeartifact_repository_permissions_policy" "codeartifact_policy" {
  repository = var.codeartifact_repository 
  domain = var.codeartifact_domain 
  policy_document = data.aws_iam_policy_document.codeartifact_policy.json
}

data "aws_iam_policy_document" "codeartifact_policy" {
  statement {
    principals {
      type       = "AWS"
      identifiers = var.user_arn
    }
    actions = [
      "codeartifact:GetAuthorizationToken",
      "codeartifact:GetRepositoryEndpoint",
      "codeartifact:ReadFromRepository",
      "codeartifact:PublishPackageVersion",
      "sts:GetServiceBearerToken"
    ]
    resources = [
      var.codeartifact_repo_arn,
      "${var.codeartifact_repo_arn}/*",
    ]

  }
}

resource "aws_codeartifact_domain_permissions_policy" "codeartifact_domain_policy" {
  domain = var.codeartifact_domain
  policy_document = data.aws_iam_policy_document.codeartifact_domain_policy.json
}

data "aws_iam_policy_document" "codeartifact_domain_policy" {
  statement {
    principals {
      type       = "AWS"
      identifiers = var.user_arn
    }
    actions = [
      "codeartifact:GetAuthorizationToken",
      "codeartifact:GetRepositoryEndpoint",
      "codeartifact:ReadFromRepository",
      "codeartifact:PublishPackageVersion",
      "sts:GetServiceBearerToken"
    ]
    resources = [
      var.codeartifact_domain_arn,
      "${var.codeartifact_domain_arn}/*",
    ]

  }
}


