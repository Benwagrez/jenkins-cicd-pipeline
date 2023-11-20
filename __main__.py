"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
from jenkins import init_jenkins
from network import init_network

awsConfig = pulumi.Config("aws")
region = awsConfig.get("region")

config = pulumi.Config()
network = config.require_object("networkvars")
ssh_key = config.get("ssh_key")
vpc = network["value"]["vpccidr"]
subnet = network["value"]["subnetcidr"]
print("SSH Key:",ssh_key)
print("Networking configuration:",vpc, subnet)

network = init_network(vpc, subnet)
jenkins = init_jenkins(ssh_key, network["subnet_id"],network["security_group"])

# # Export jenkins attributes -- Augment functions to return dict with values to pull into exports
pulumi.export('Server IP', jenkins["jenkins_public_ip"])
pulumi.export('Server DNS', jenkins["jenkins_public_dns"])
pulumi.export('AWS Region', region)