"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
from jenkins import init_jenkins
from network import init_network

awsConfig = pulumi.Config("aws")
region = awsConfig.get("region")

config = pulumi.Config()
network = config.require_object("networkvars")
vpc = network["value"]["vpccidr"]
subnet = network["value"]["subnetcidr"]

print("Networking configuration:",vpc, subnet)

subnet_id = init_network(vpc, subnet)
jenkins = init_jenkins(subnet_id)

# # Export jenkins attributes -- Augment functions to return dict with values to pull into exports
pulumi.export('Server IP', jenkins)
pulumi.export('AWS Region', region)