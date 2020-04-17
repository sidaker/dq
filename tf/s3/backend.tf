terraform {
  backend "s3" {
    # Replace this with your bucket name!
    bucket         = "advitek-terraform-up-and-running-state"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-2"

    # Replace this with your DynamoDB table name!
    dynamodb_table = "advitek-terraform-up-and-running-locks"
    encrypt        = true
  }
}
