# Infrastructure

## Overview

This repository contains the infrastructure as code (IaC) using `Terraform` to deploy the following resoureces:

- `AWS s3` bucket
- `AWS CodeArtifact` repository

### AWS s3 bucket

The s3 bucket is used to store raw and processed data, acting as a data lake.

### AWS CodeArtifact

The CodeArtifact is used to store and manage the python packages used in the project. The packages include:

- `data_pipeline` -> package containing code to process data in offline model training and online model serving
- `model_pipeline` -> package containing code to train, test, and validate models before deploying to the model registry and serving
