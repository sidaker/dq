provider "aws" {
  region = "us-east-2"
}

/*
The general syntax for creating a resource in Terraform is:
resource "<PROVIDER>_<TYPE>" "<NAME>" {
  [CONFIG ...]
}

# curl http://<EC2_INSTANCE_PUBLIC_IP>:8080

*/
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.secinstance.id]
/*
When you launch an EC2 Instance, you have the option of passing either a shell script or cloud-init directive to User Data,
 and the EC2 Instance will execute it during boot. 
*/
  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World" > index.html
              nohup busybox httpd -f -p 8080 &
              EOF


  tags = {
    Name = "terraform-example-sid-ec2"
  }
}

/* Create Security group to allow traffic on port 8080 from any ip address */
resource "aws_security_group" "secinstance" {
  name = "terraform-example-sid-sec-instance"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# tell the EC2 Instance to actually use it by passing the ID of the security group into the vpc_security_group_ids argument of the aws_instance resource. 


/*
In a real-world use case, you’d probably build the web server using a web framework like Ruby on Rails or Django, 
but to keep this example simple, let’s run a dirt-simple web server that always returns the text “Hello, World”.
This is a Bash script that writes the text “Hello, World” into index.html and runs a tool called busybox 
(which is installed by default on Ubuntu) to fire up a web server on port 8080 to serve that file. 
I wrapped the busyboxcommand with nohup and & so that the web server runs permanently in the background, 
whereas the Bash script itself can exit.
The <<-EOF and EOF are Terraform’s heredoc syntax, which allows you to create multiline strings without having to 
insert newline characters all over the place.
*/