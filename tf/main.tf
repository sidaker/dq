/*
This tells Terraform that you are going to be using AWS as your provider and
that you want to deploy your infrastructure into the eu-west-2 region.
The general syntax for creating a resource in Terraform is:
resource "<PROVIDER>_<TYPE>" "<NAME>" {
  [CONFIG ...]
}

Run terraform init the first time.
terraform init
terraform plan
terraform apply
terraform destroy
*/

provider "aws" {
  region = "eu-west-2"
}
