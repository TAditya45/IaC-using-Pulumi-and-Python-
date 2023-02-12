# IaC-using-Pulumi-and-Python-

A code which is written  to set up a VPC, subnets, internet gateway, security group, and an EC2 instance that runs an Nginx Docker container. The EC2 instance is launched in an Auto Scaling Group with two instances. The instances are in the private subnets and are targetted by a Load Balancer in the public subnet.

Whenever we  open the Load Balancer's DNS in a web browser, the Nginx welcome page will open.
