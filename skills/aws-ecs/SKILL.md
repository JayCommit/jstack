---
name: aws-ecs
description: "Use when you create or deploy an ECS service. Prefer Fargate, split the task role from the execution role, and put the service behind a load balancer with a deployment circuit breaker."
license: MIT
---

# Elastic Container Service

Run the service on Fargate in private subnets. The task role is what the application can do. The execution role is what ECS can do to start the task.

## Use when

- You create an ECS cluster, a task definition or a service.
- You change a deploy, a target group or the roles on a task.
- Someone proposes EC2 launch type, a public IP on the task, or one role for both jobs.
- A deploy is stuck and the circuit breaker has not been turned on.

## Steps

1. Read the service before you change it. Run `aws ecs describe-services --cluster ecs-example --services app-example --region eu-west-2` and `aws ecs describe-task-definition --task-definition app-example --region eu-west-2`. Record the launch type, the roles, the desired count and the last deployment status. Follow `principle-observe-before-you-fix`.

2. Use Fargate unless the workload needs a GPU, a device, or a host you must log on to. An EC2 capacity provider is its own design and its own cost. Do not copy the production CPU and memory into dev or test. Pick a supported Fargate pair. Follow `principle-cost-awareness` and `aws-cost-review`.

3. Put tasks in the private subnets from `aws-vpc`. Set `assignPublicIp` to `DISABLED`. Give the task security group its port from the load balancer security group only.

4. Split the roles. The execution role may pull from ECR, write logs and read the secrets the task definition injects. The task role is the application's API calls, written as in `aws-iam-least-privilege`. Do not attach the task role to the execution role, and do not use the task role as an instance profile.

5. Inject secrets from Secrets Manager or Parameter Store with `valueFrom`. Do not put the secret in `environment`. Follow `aws-secrets-ssm`. The image tag is a digest or a release you have reviewed. `latest` is not a release.

6. Put the service behind an Application Load Balancer. The target group type is `ip`. A target type of `instance` stays empty on Fargate. The health check path returns success only when the app is ready. Listen on 443.

7. Turn on the deployment circuit breaker and rollback. Keep the minimum healthy percent at 100 for a production service unless the change record says the service can drop a task. A deploy that cannot roll back is not ready.

   ```bash
   aws ecs update-service --cluster ecs-example --service app-example --region eu-west-2 --deployment-configuration "deploymentCircuitBreaker={enable=true,rollback=true},maximumPercent=200,minimumHealthyPercent=100"
   ```

8. Watch the deployment. `aws ecs describe-services` must show the new deployment `rolloutState` as `COMPLETED`, and the target group must show healthy targets, before you start another change. A failed deploy should already have rolled back. If it has not, stop and read the stopped task reason. Follow `principle-observe-before-you-fix`.

9. Authenticate the pipeline with the GitHub OIDC role from `aws-iam-least-privilege`. The deploy role can register a task definition and update this service. It cannot administer IAM. Follow `principle-no-static-credentials`. If Terraform applies the service, follow `terraform-plan-review` and `terraform-state-backends`. Name the account, the cluster, the service and the pipeline. Follow `principle-change-safety`.

## Safety checks

- The launch type is Fargate, or the change record names the device or GPU that forced EC2.
- Tasks have no public IP. The task security group accepts only the load balancer group.
- Execution role and task role are different. The secret is not in `environment`.
- The image is a digest or a reviewed tag. The target type is `ip`.
- The circuit breaker is on and rollback is on. Minimum healthy percent is 100, or the exception is written down.
- The pipeline role is federated and cannot change IAM.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Keep the previous task definition ARN. `aws ecs update-service --task-definition` back to that ARN is the rollback, and the circuit breaker should do it on a failed deploy.
2. Rehearse that update on a non-production service before you depend on it in production.
3. Do not delete the previous task definition until the new rollout has stayed healthy through a check you named.

## Done when

- The service is at the reviewed task definition, with healthy targets.
- Roles, subnets and the circuit breaker match this skill.
- The change is verified on this service before anyone promotes it.
