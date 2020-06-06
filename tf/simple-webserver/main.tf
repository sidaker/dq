
provider "aws" {
  region = "eu-west-2"
}

# <<-EOF and EOF are Terraform’s heredoc syntax, which allows you to create
# multiline strings without having to insert newline characters all over the place.

resource "aws_instance" "example" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = "t2.micro"

  # Create a Security Group and attach its ID to the EC2 instance.
  /* When you add a reference from one resource to another, you create an implicit dependency.
  Terraform parses these dependencies, builds a dependency graph from them, and uses that to
   automatically determine in which order it should create resources.
  */
  vpc_security_group_ids = [aws_security_group.instance.id]

  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World" > index.html
              nohup busybox httpd -f -p 8080 &
              EOF

  tags = {
    Name = "terraform-example"
  }
}


# Create Security group to allow inbound traffic on port 8080.
/*
By default, AWS does not allow any incoming or outgoing traffic from an EC2 Instance.
To allow the EC2 Instance to receive traffic on port 8080, you need to create a security group:
allows incoming TCP requests on port 8080 from the CIDR block 0.0.0.0/0.
CIDR blocks are a concise way to specify IP address ranges.
For example, a CIDR block of 10.0.0.0/24 represents all IP addresses between 10.0.0.0 and 10.0.0.255.
The CIDR block 0.0.0.0/0 is an IP address range that includes all possible IP addresses,
so this security group allows incoming requests on port 8080 from any IP
*/

resource "aws_security_group" "instance" {
  name = "terraform-example-instance"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

/*
You need to attach the security group id(known after you apply) to the EC2 instance.
Simply creating a security group isn’t enough; you also need to tell the EC2 Instance
to actually use it by passing the ID of the security group into the vpc_security_group_ids argument of the aws_instance resource.
To access the ID of the security group resource, you are going to need to use a resource attribute reference,
which uses the following syntax:
<PROVIDER>_<TYPE>.<NAME>.<ATTRIBUTE>

The security group exports an attribute called id , so the expression to reference it will look like this:
aws_security_group.instance.id


*/
