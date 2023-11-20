# Jenkins CICD Pipeline
This is a pulumi based deployment for a Jenkins EC2 instance.

## Prerequisites
The following items are prerequisites for this deployment.
<ul>
    <li>An account with Pulumi Cloud</li>
    <li>Pulumi as a registered idP on AWS</li>
    <li>An AWS role with sufficient permissions for Pulumi to assume</li>
</ul>

## Deployment Overview

This deployment relies on a Pulumi environment setup on the cloud to reference the AWS Pulumi idP for authentication. Refer to [Pulumi ESC](https://www.pulumi.com/product/esc/) for more information. Run pulumi up to deploy.

## Licensing

Everything is licensed under the MIT license, feel free to repurpose my code for whatever you'd like.

## Contact

Reach out to me below for any questions:

Email: benwagrez@gmail.com
LinkedIn: https://www.linkedin.com/in/benwagrez/