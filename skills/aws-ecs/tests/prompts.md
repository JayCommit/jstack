# Prompts for aws-ecs

Example asks for `aws-ecs`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create an ECS cluster, a task definition or a service.

### Expected for ask 1

- Load `aws-ecs` and follow that file through its own done-when.
- Step: Read the service before you change it. Run `aws ecs describe-services --cluster ecs-example --services app-example --region eu-west-2` and `aws ecs describe-task-definition --task-definition app-example --region eu-west-2`. Record the launch type, the roles, the desired count and the last deployment status. Follow `principle-observe-before-you-fix`.
- Check: The launch type is Fargate, or the change record names the device or GPU that forced EC2.
- Done when: The service is at the reviewed task definition, with healthy targets.

## Ask 2

Use Fargate unless the workload needs a GPU, a device, or a host you must log on to.

### Expected for ask 2

- Load `aws-ecs` and follow that file through its own done-when.
- Step: Use Fargate unless the workload needs a GPU, a device, or a host you must log on to. An EC2 capacity provider is its own design and its own cost. Do not copy the production CPU and memory into dev or test. Pick a supported Fargate pair. Follow `principle-cost-awareness` and `aws-cost-review`.
- Check: Tasks have no public IP. The task security group accepts only the load balancer group.
- Done when: Roles, subnets and the circuit breaker match this skill.
