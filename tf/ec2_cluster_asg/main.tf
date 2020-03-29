provider "aws" {
  region = "us-east-2"
}


/* Create Security group to allow traffic on port 8080 from any ip address */
resource "aws_security_group" "secinstance" {
  name = "terraform-example-sid-sec-instance"

  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

