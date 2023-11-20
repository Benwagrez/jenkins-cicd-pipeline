import pulumi
import pulumi_aws as aws

def init_jenkins(ssh_key,subnet,security_group) -> pulumi.Output[str]:
	aws_key = aws.ec2.KeyPair(
		"generated",
		key_name="JenkinsCICDKey",
		public_key=ssh_key,
    )
	user_data = open('ec2config.tpl')
	user_data_reader = user_data.read()
	ami = aws.ssm.get_parameter(name="/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2")
	jenkins = aws.ec2.Instance("Jenkins",
			key_name = aws_key.key_name,
      ami=ami.value,
      instance_type="t2.micro",
      tags={
          "Project": pulumi.get_project(),
          "Stack": pulumi.get_stack(),
          "Owner": "benwagrez@gmail.com",
          "Name": "Jenkins Instance",
      },
      user_data=user_data_reader,
      subnet_id=subnet,
			security_groups=[security_group],
      associate_public_ip_address=True
      )
	output = {
		"jenkins_public_ip": jenkins.public_ip,
		"jenkins_public_dns": jenkins.public_dns
	}
	return output