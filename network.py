import pulumi
import pulumi_aws as aws

def init_network(vpccidr: str, subnetcidr: str) -> pulumi.Output[str]:
  vpc = aws.ec2.Vpc("main",
      cidr_block=vpccidr,
      instance_tenancy="default",
      tags={
          "Project": pulumi.get_project(),
          "Stack": pulumi.get_stack(),
          "Owner": "benwagrez@gmail.com",
          "Name": "Jenkins VPC",
      })
  vpcsubnet = aws.ec2.Subnet("main",
      vpc_id=vpc.id,
      cidr_block=subnetcidr,
      tags={
          "Project": pulumi.get_project(),
          "Stack": pulumi.get_stack(),
          "Owner": "benwagrez@gmail.com",
          "Name": "Public Subnet",
      })
  gw = aws.ec2.InternetGateway("gw",
      vpc_id=vpc.id,
      tags={
          "Project": pulumi.get_project(),
          "Stack": pulumi.get_stack(),
          "Owner": "benwagrez@gmail.com",
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
          "Project": pulumi.get_project(),
          "Stack": pulumi.get_stack(),
          "Owner": "benwagrez@gmail.com",
          "Name": "allow_tls",
      })
  output = {
		"subnet_id": vpcsubnet.id,
		"security_group": allow_tls.id,
	}
  return output