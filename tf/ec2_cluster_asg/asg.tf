resource "aws_launch_configuration" "example" {
  image_id        = "ami-0c55b159cbfafe1f0"
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.secinstance.id]

  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World" > index.html
              nohup busybox httpd -f -p ${var.server_port} &
              EOF

   lifecycle {
    create_before_destroy = true
  }
           
}


resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.example.name
  vpc_zone_identifier  = data.aws_subnet_ids.default.ids

  target_group_arns = [aws_lb_target_group.asg.arn]
  health_check_type = "ELB"


  min_size = 2
  max_size = 10

  tag {
    key                 = "Name"
    value               = "terraform-asg-example"
    propagate_at_launch = true
  }
}

/*
Every Terraform resource supports several lifecycle settings that configure how that resource is 
created, updated, and/or deleted. A particularly useful lifecycle setting is create_before_destroy. 
If you set create_before_destroy to true, Terraform will invert the order in which it replaces resources, 
creating the replacement resource first (including updating any references that were pointing at the old resource to
 point to the replacement) and then deleting the old resource. 

 There’s also one other parameter that you need to add to your ASG to make it work: subnet_ids. 
 This parameter specifies to the ASG into which VPC subnets the EC2 Instances should be deployed.
 You could hardcode the list of subnets, but that won’t be maintainable or portable, so a better option is to use
  data sources to get the list of subnets in your AWS account.
*/