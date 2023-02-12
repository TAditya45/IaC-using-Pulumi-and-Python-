import pulumi
import pulumi_aws as aws

#creating an Amazon Virtual Private Cloud 
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16",
    tags={
        "Name": "my-vpc",
    })

#creating Private Subnet-1
private_subnet_1 = aws.ec2.Subnet("private-subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    tags={
        "Name": "private-subnet-1",
    })

#creating Private Subnet-2
private_subnet_2 = aws.ec2.Subnet("private-subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    tags={
        "Name": "private-subnet-2",
    })

#creating Public Subnet-1
public_subnet = aws.ec2.Subnet("public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",
    map_public_ip_on_launch=True,
    tags={
        "Name": "public-subnet",
    })

# creating an Internet Gateway in AWS and attaching it to a VPC
internet_gateway = aws.ec2.InternetGateway("internet-gateway",
    tags={
        "Name": "internet-gateway",
    })

#creating a VPC Gateway Attachment between the Internet Gateway and the VPC. 
igw_attachment = aws.ec2.VpcGatewayAttachment("igw-attachment",
    internet_gateway_id=internet_gateway.id,
    vpc_id=vpc.id)

#Creating Route table 
route_table = aws.ec2.RouteTable("route-table",
    vpc_id=vpc.id,
    routes=[{
        "cidr_block": "0.0.0.0/0",
        "gateway_id": igw_attachment.id,
    }],
    tags={
        "Name": "route-table",
    })

#creating a new association between a subnet and a route table
private_route_table_association_1 = aws.ec2.RouteTableAssociation("private-route-table-association-1",
    route_table_id=route_table.id,
    subnet_id=private_subnet_1.id)

private_route_table_association_2 = aws.ec2.RouteTableAssociation("private-route-table-association-2",
    route_table_id=route_table.id,
    subnet_id=private_subnet_2.id)

#Creating security group for EC2 Instances 
security_group = aws.ec2.SecurityGroup("security-group",
    vpc_id=vpc.id,
    ingress=[{
        "protocol": "tcp",
        "from_port": 80,
        "to_port": 80,
        "cidr_blocks": ["0.0.0.0/0"],
    }],
    tags={
        "Name": "security-group",
    })

#running Docker Container for every EC2 Instance 
user_data = """#!/bin/bash
docker run --name nginx -d -p 80:80 nginx
instance_type = "t2.micro"
asg = aws.autoscaling.Group("asg",
    launch_template={
        "id": aws.ec2.LaunchTemplate("launch-template",
            launch_template_data={
                "instance_type": instance_type,
                "security_group_ids": [security_group.id],
                "subnet_id": private_subnet_1.id,
                "user_data": user_data,
            }
        ).id,
        "version": "$Latest",
    },
    min_size=2,
    max_size=2,
    desired_capacity=2,
    target_group_arns=[],
    vpc_zone_identifier=[private_subnet_1.id, private_subnet_2.id],
    tags={
        "Name": "asg",
    },
)

#Creating EC2 load balancer for Public subnet
load_balancer = aws.elbv2.LoadBalancer("load-balancer",
    internal=False,
    security_groups=[security_group.id],
    subnets=[public_subnet.id],
)

listener = aws.elbv2.Listener("listener",
    default_actions=[{
        "type": "forward",
        "target_group_arn": aws.elbv2.TargetGroup("target-group",
            port=80,
            protocol="HTTP",
            target_type="instance",
            vpc_id=vpc.id,
        ).arn,
    }],
    load_balancer_arn=load_balancer.arn,
    port=80,
    protocol="HTTP",
)

pulumi.export("load_balancer_dns", load_balancer.dns_name)