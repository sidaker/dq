/*
A data source represents a piece of read-only information that is fetched from the provider (in this case, AWS) every time 
you run Terraform. Adding a data source to your Terraform configurations does not create anything new; 
it’s just a way to query the provider’s APIs for data and to make that data available to the rest of your Terraform code. 

data "<PROVIDER>_<TYPE>" "<NAME>" {
  [CONFIG ...]
}

*/

data "aws_vpc" "default" {
  default = true
}


data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id
}

