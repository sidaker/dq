provider "aws" {
  region = "us-east-2"
}


resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.secinstance.id]

  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World" > index.html
              nohup busybox httpd -f -p ${var.server_port} &
              EOF


  tags = {
    Name = "terraform-example-sid-ec2"
  }
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

