"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import base64

vpc = aws.ec2.Vpc("main",
    cidr_block="10.0.0.0/16",
    instance_tenancy="default",
    tags={
        "Name": "Jenkins VPC",
    })

vpcsubnet = aws.ec2.Subnet("main",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    tags={
        "Name": "Main Subnet",
    })


gw = aws.ec2.InternetGateway("gw",
    vpc_id=vpc.id,
    tags={
        "Name": "Internet Gateway",
    })

allow_tls = aws.ec2.SecurityGroup("allowTls",
    description="Allow TLS inbound traffic",
    vpc_id=vpc.id,
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        description="SSH from all",
        from_port=22,
        to_port=22,
        protocol="tcp",
        cidr_blocks=["0.0.0.0/0"],
        ipv6_cidr_blocks=["::/0"],
    ),
    aws.ec2.SecurityGroupIngressArgs(
        description="Jenkins 8080 from all",
        from_port=8080,
        to_port=8080,
        protocol="tcp",
        cidr_blocks=["0.0.0.0/0"],
        ipv6_cidr_blocks=["::/0"],
    )],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        from_port=0,
        to_port=0,
        protocol="-1",
        cidr_blocks=["0.0.0.0/0"],
        ipv6_cidr_blocks=["::/0"],
    )],
    tags={
        "Name": "allow_tls",
    })

ubuntu = aws.ec2.get_ami(most_recent=True,
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"],
        ),
        aws.ec2.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"],
        ),
    ],
    owners=["099720109477"])

user_data = open('ec2config.tpl')
user_data_reader = user_data.read()
jenkins = aws.ec2.Instance("jenkins",
    ami=ubuntu.id,
    instance_type="t3.micro",
    tags={
        "Name": "HelloWorld",
    },
    user_data=user_data_reader,
    subnet_id=vpcsubnet.id,
    associate_public_ip_address=True
    )

# Export jenkins attributes
pulumi.export('Server IP', jenkins.public_ip)
pulumi.export('Server IP', jenkins.public_dns)
