---
name: aws-vpc
description: "Use when you add or change a VPC, subnet, route, NAT gateway, VPC endpoint, security group or Transit Gateway. Keep data subnets private and send S3 and DynamoDB through gateway endpoints."
license: MIT
---

# VPC networking

Keep application and data subnets off the internet gateway. Use security groups for the path between them. Price every NAT gateway and interface endpoint.

## Use when

- You create a VPC, a subnet, a route table or an internet gateway.
- You add a NAT gateway, a gateway endpoint, an interface endpoint or a Transit Gateway attachment.
- You change a security group or a network ACL.
- Two VPCs need to talk, or a peering mesh is growing.

## Steps

1. Read the VPC before you change it. Run `aws ec2 describe-vpcs --vpc-ids vpc-example`, `aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-example`, `aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-example` and `aws ec2 describe-security-groups --filters Name=vpc-id,Values=vpc-example`. Record CIDRs, which route tables have an internet gateway, and which have a NAT gateway. Follow `principle-observe-before-you-fix`.

2. Pick a CIDR from RFC 1918 that does not overlap a network you will peer or attach to a Transit Gateway. A VPC `10.0.0.0/16` with public `10.0.0.0/24` and `10.0.1.0/24`, application `10.0.10.0/24` and `10.0.11.0/24`, and data `10.0.20.0/24` and `10.0.21.0/24` is the shape. Spread subnets across two Availability Zones. Turn on DNS hostnames and DNS resolution.

3. Give only the public subnets a route to the internet gateway. Those subnets hold load balancers and NAT gateways. Application subnets route `0.0.0.0/0` to a NAT gateway, or to no default route when the workload does not call the internet. Data subnets have no internet gateway and no NAT route. Set `MapPublicIpOnLaunch` to false on application and data subnets.

4. Use one NAT gateway per Availability Zone when the application must survive an AZ failure. A single NAT gateway is a cost choice and a single-AZ dependency. Record which one this VPC is, and the hourly plus per-GB estimate. Follow `aws-cost-review` and `principle-cost-awareness`.

5. Add gateway endpoints for S3 and DynamoDB on the private route tables. They have no hourly charge. Add an interface endpoint only for an API the private subnets call and that would otherwise go through NAT. Each interface endpoint is hourly per AZ plus data. Record that cost. Security group the interface endpoint to TCP 443 from the workload security group.

6. Use security groups as the control. They are stateful. An application group accepts its port from the load balancer group only. A data group accepts its port from the application group only. Do not open `0.0.0.0/0` on a workload port. A network ACL is stateless. Add one for a coarse deny you can name. Do not copy every security group rule into an ACL.

   ```bash
   aws ec2 authorize-security-group-ingress --group-id sg-app-example --protocol tcp --port 8080 --source-group sg-alb-example
   ```

7. Prefer a Transit Gateway once more than a pair of VPCs must communicate, or when several accounts share one network. Peering is not transitive. Do not build a mesh of peering connections. Put the attachment in its own subnets. Turn on appliance mode only for an inspection VPC that the design already chose. A new AWS Network Firewall is its own change and a cost line.

8. Turn on VPC flow logs to the log archive account, or to a log group with a retention you set. Follow `aws-cloudwatch`. Unbounded flow logs are a cost change. Follow `principle-cost-awareness`.

9. If Terraform applies the network, follow `terraform-plan-review` and `terraform-state-backends`. Name the account, the VPC, the route tables and the pipeline. One network change. Follow `principle-change-safety`. Codify a console route or remove it. Follow `principle-everything-as-code`.

## Safety checks

- Application and data subnets have no route to an internet gateway. `MapPublicIpOnLaunch` is false there.
- The CIDR does not overlap a network this VPC will join.
- S3 and DynamoDB use gateway endpoints on the private route tables.
- Each new NAT gateway and interface endpoint is in the cost estimate.
- Workload security groups do not accept `0.0.0.0/0`. The data group accepts only the application group.
- A peering mesh is not how a third VPC is being attached.
- Flow logs have a destination and a retention.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Keep the previous route table and the previous security group rules. Rehearse the reverse change in a non-production VPC.
2. Delete a new endpoint or a new NAT gateway by a reviewed change. Do not delete the only NAT gateway while private subnets still route to it.
3. Stop if the reverse plan disconnects the path you use to reach the hosts. Fix the path first.

## Done when

- The routes match the public, application and data split above.
- Security groups name the peer group, not the internet.
- Endpoints and NAT match the design, and the cost is on the change.
- The change is verified in this VPC before anyone copies it to another account.
