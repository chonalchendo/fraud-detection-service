provider "aws" {
  region = "eu-west-1"
}

locals {
  bucket_name = "fraud-detection-system"
  tags = {
    project = "fraud-detection-system"
  }
}

module "base" {
  source = "./base"
  bucket_name = local.bucket_name
  tags = local.tags
  codeartifact_domain = "fraud-detection-domain"
  codeartifact_repository = "python-packages"
}

module "iam" {
  source = "./iam"
  name = "fraud-detection-system"
  tags = local.tags
  bucket_name = module.base.bucket_name 
  bucket_arn = module.base.bucket_arn
}

resource "aws_iam_user" "spacelift_user" {
  name = "spacelift-user"
}

resource "aws_iam_user_login_profile" "spacelift_user_login_profile" {
  user = aws_iam_user.spacelift_user.name
}

