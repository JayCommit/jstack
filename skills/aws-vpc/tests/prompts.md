# Prompts for aws-vpc

Example asks for `aws-vpc`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create a VPC, a subnet, a route table or an internet gateway.

### Expected for ask 1

- Load `aws-vpc` and follow that file through its own done-when.
- Step: Read the VPC before you change it. Run `aws ec2 describe-vpcs --vpc-ids vpc-example`, `aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-example`, `aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-example` and `aws ec2 describe-security-groups --filters Name=vpc-id,Values=vpc-example`. Record CIDRs, which route tables have an internet gateway, and which have a NAT gateway. Follow `principle-observe-before-you-fix`.
- Check: Application and data subnets have no route to an internet gateway. `MapPublicIpOnLaunch` is false there.
- Done when: The routes match the public, application and data split above.

## Ask 2

Pick a CIDR from RFC 1918 that does not overlap a network you will peer or attach to a Transit Gateway.

### Expected for ask 2

- Load `aws-vpc` and follow that file through its own done-when.
- Step: Pick a CIDR from RFC 1918 that does not overlap a network you will peer or attach to a Transit Gateway. A VPC `10.0.0.0/16` with public `10.0.0.0/24` and `10.0.1.0/24`, application `10.0.10.0/24` and `10.0.11.0/24`, and data `10.0.20.0/24` and `10.0.21.0/24` is the shape. Spread subnets across two Availability Zones. Turn on DNS hostnames and DNS resolution.
- Check: The CIDR does not overlap a network this VPC will join.
- Done when: Security groups name the peer group, not the internet.
