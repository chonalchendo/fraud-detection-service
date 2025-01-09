provider "aws" {
  region = "eu-west-1"
}

locals {
  bucket_name = "fraud-detection-system"
  codeartifact_domain = "fraud-detection-domain"
  codeartifact_repository = "python-packages"
  user_arn = ["arn:aws:iam::061051215402:user/fraud-detection-system",]
  tags = {
    project = "fraud-detection-system"
  }
}

module "base" {
  source = "./base"
  bucket_name = local.bucket_name
  tags = local.tags
  codeartifact_domain = local.codeartifact_domain 
  codeartifact_repository = local.codeartifact_repository 
}

module "iam" {
  source = "./iam"
  user_name = "fraud-detection-system"
  tags = local.tags
  bucket_name = module.base.bucket_name 
  bucket_arn = module.base.bucket_arn
  user_arn = local.user_arn
  codeartifact_domain = module.base.codeartifact_domain
  codeartifact_repository = module.base.codeartifact_repository
  codeartifact_repo_arn = module.base.codeartifact_repo_arn
  codeartifact_domain_arn = module.base.codeartifact_domain_arn
}

