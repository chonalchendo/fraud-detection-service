variable "bucket_name" {
  type = string
  description = "The name of the project s3 bucket"
}

variable "tags" {
  type = map
  description = "The tags to apply to the resources"
}

variable "codeartifact_domain" {
  type = string
  description = "The name of the CodeArtifact domain"
}

variable "codeartifact_repository" {
  type = string
  description = "The name of the CodeArtifact repository"
}

resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_ownership_controls" "bucket-ownership-controls" {
  bucket = aws_s3_bucket.bucket.bucket
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "bucket-acl" {
  depends_on = [aws_s3_bucket_ownership_controls.bucket-ownership-controls]

  bucket = aws_s3_bucket.bucket.id
  acl    = "private"
}

# CodeArtifact for Python packages
resource "aws_codeartifact_domain" "domain" {
  domain = var.codeartifact_domain  # top-level domain name
}

resource "aws_codeartifact_repository" "python_packages" {
  repository = var.codeartifact_repository # repository name
  domain     = var.codeartifact_domain 

  external_connections {
    external_connection_name = "public:pypi"  # For Python packages
  }

  description = "Repository for fraud detection Python packages"
}

output "bucket_name" {
  value = aws_s3_bucket.bucket.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.bucket.arn
}

output "codeartifact_domain" {
  value = aws_codeartifact_domain.domain.domain
}

output "codeartifact_repository" {
  value = aws_codeartifact_repository.python_packages.repository
}

output "codeartifact_repo_arn" {
  value = aws_codeartifact_repository.python_packages.arn
}

output "codeartifact_domain_arn" {
  value = aws_codeartifact_domain.domain.arn
}
