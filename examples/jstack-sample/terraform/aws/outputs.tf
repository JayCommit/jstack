output "vpc_id" {
  description = "Id of the sample VPC."
  value       = aws_vpc.this.id
}

output "private_subnet_id" {
  description = "Id of the sample private subnet."
  value       = aws_subnet.private.id
}
