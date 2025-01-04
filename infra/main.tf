provider "aws" {
  region = "eu-west-1"
}

locals {
  bucket_name = "fraud-detection-system"
  user_arn = ["arn:aws:iam::061051215402:user/fraud-detection-system",]
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
  user_arn = local.user_arn
}

