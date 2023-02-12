# IaC-using-Pulumi-and-Python-

A code which is written  to set up a VPC, subnets, internet gateway, security group, and an EC2 instance that runs an Nginx Docker container. The EC2 instance is launched in an Auto Scaling Group with two instances. The instances are in the private subnets and are targetted by a Load Balancer in the public subnet.

Whenever we  open the Load Balancer's DNS in a web browser, the Nginx welcome page will open.

The   Infrastructe  Consist the Following in it's enviornment 

A Virtual Private Cloud (VPC) with a specified CIDR block and name "my-vpc".

Three subnets within the VPC - two private subnets and one public subnet. Each subnet has a specified CIDR block and name.

An internet gateway and a VPC gateway attachment that allows communication between the VPC and the internet.

A route table with a default route to the internet gateway. The route table is associated with the two private subnets.

A security group for the EC2 instances, which allows incoming TCP traffic on port 80.

An EC2 Auto Scaling Group (ASG) with a launch template that launches 2 EC2 instances with the specified instance type and user data, which runs a Docker container with the Nginx image. The ASG is associated with the two private subnets and the security group.

An EC2 load balancer that forwards incoming HTTP traffic to the instances in the ASG, and a listener for the load balancer that listens for incoming traffic on port 80.
