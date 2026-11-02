# Prompts for aws-codepipeline-awareness

Example asks for `aws-codepipeline-awareness`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I open a CodePipeline pipeline, a CodeBuild project or a CodeConnections connection.

### Expected for ask 1

- Load `aws-codepipeline-awareness` and follow that file through its own done-when.
- Step: Read the pipeline and the projects before you change them. Run `aws codepipeline get-pipeline --name example` and `aws codebuild batch-get-projects --names example`. Record the pipeline type, the source action, each build project's environment and the service roles. Follow `principle-observe-before-you-fix`.
- Check: You read the pipeline JSON and the project environment before editing.
- Done when: The pipeline that ships is the one you read, or the replacement has deployed once beside it.

## Ask 2

Keep a pipeline that already deploys.

### Expected for ask 2

- Load `aws-codepipeline-awareness` and follow that file through its own done-when.
- Step: Keep a pipeline that already deploys. Fix it in place when the failure is in that pipeline. Move it only when the change record says why, and move it as its own change. Do not migrate the pipeline and change the application in the same release. Follow `principle-change-safety`.
- Check: A new deploy is GitHub Actions with OIDC, or the change record says why it stays in CodePipeline.
- Done when: The build role, the source connection and the approval match this skill.
