# Prompts for gitops-argocd-flux

Example asks for `gitops-argocd-flux`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add Argo CD or Flux, or you add an app to either.

### Expected for ask 1

- Load `gitops-argocd-flux` and follow that file through its own done-when.
- Step: Read what the cluster is already running. For Argo CD, run `argocd app list` and `argocd app get app-example`. For Flux, run `flux get kustomizations -A`. Record the revision, whether prune is on, and whether the app is healthy. Follow `principle-observe-before-you-fix`. Do not install the other controller over apps this one already reconciles.
- Check: One controller reconciles these apps.
- Done when: The app is healthy at the revision you merged.

## Ask 2

Pick one controller per set of apps.

### Expected for ask 2

- Load `gitops-argocd-flux` and follow that file through its own done-when.
- Step: Pick one controller per set of apps. Argo CD and Flux reconciling the same path will fight. A migration from one to the other is its own change, after the new controller is proven on a non-production cluster.
- Check: Production is pinned to a tag or a commit. The digest matches the digest that passed in the lower environment.
- Done when: The production overlay runs the same digest you verified in the lower environment.
