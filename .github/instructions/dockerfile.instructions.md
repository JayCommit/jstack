---
applyTo: "**/Dockerfile,**/Dockerfile.*"
---

# Dockerfile

Follow `skills/k8s-dockerfile-hardening/SKILL.md`. Build in stages, run as a numeric non-root user, and pin every `FROM` by digest. Add a `.dockerignore` before a `COPY` of the build context.
