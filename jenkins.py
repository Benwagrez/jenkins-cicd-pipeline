import pulumi
import pulumi_aws as aws

def init_jenkins(subnet) -> pulumi.Output[str]:
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
      instance_type="t2.micro",
      tags={
          "Project": pulumi.get_project(),
          "Stack": pulumi.get_stack(),
          "Owner": "benwagrez@gmail.com",
          "Name": "Jenkins Instance",
      },
      user_data=user_data_reader,
      subnet_id=subnet,
      associate_public_ip_address=True
      )
  return jenkins.public_ip