mock_provider "aws" {}

run "plan_network" {
  command = plan

  variables {
    region = "eu-west-2"
  }

  assert {
    condition     = aws_vpc.this.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR must be 10.0.0.0/16."
  }

  assert {
    condition     = aws_subnet.private.map_public_ip_on_launch == false
    error_message = "Private subnet must not map a public IP on launch."
  }

  assert {
    condition     = aws_vpc_endpoint.s3.service_name == "com.amazonaws.eu-west-2.s3"
    error_message = "S3 gateway endpoint must target com.amazonaws.eu-west-2.s3."
  }

  assert {
    condition     = aws_vpc_endpoint.s3.vpc_endpoint_type == "Gateway"
    error_message = "S3 endpoint must be a gateway endpoint."
  }
}

# Ingress and route sets are unknown during plan under mock_provider.
# This apply stays on the mock. It does not call AWS.
run "mock_apply_network" {
  command = apply

  variables {
    region = "eu-west-2"
  }

  assert {
    condition     = length(aws_security_group.app.ingress) == 0
    error_message = "Application security group must have no ingress rule."
  }

  assert {
    condition = length([
      for route in aws_route_table.private.route : route
      if route.cidr_block == "0.0.0.0/0"
    ]) == 0
    error_message = "Private route table must not route 0.0.0.0/0."
  }
}
