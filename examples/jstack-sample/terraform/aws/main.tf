variable "region" {
  type        = string
  description = "AWS region for the sample VPC."
  default     = "eu-west-2"

  validation {
    condition     = contains(["eu-west-2"], var.region)
    error_message = "region must be eu-west-2."
  }
}

resource "aws_vpc" "this" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "private" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = "10.0.20.0/24"
  availability_zone       = "eu-west-2a"
  map_public_ip_on_launch = false
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.this.id

  # No route block. This table must not send 0.0.0.0/0 anywhere.
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.this.id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private.id]
}

resource "aws_security_group" "app" {
  name        = "example-app"
  description = "Private application group for the sample VPC."
  vpc_id      = aws_vpc.this.id

  egress {
    description = "Traffic that stays inside the sample VPC."
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.this.cidr_block]
  }
}
