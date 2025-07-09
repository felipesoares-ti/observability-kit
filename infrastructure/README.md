# Infraestrutura GitOps

- Diretório `base/`: manifests e configs base para todos os ambientes.
- Diretório `overlays/`: customizações por ambiente (dev, prod, etc).
- O diretório `helm/` na raiz foi removido. Utilize apenas `infrastructure/helm/` para charts customizados.
- Os manifests do Kubernetes estão centralizados em `infrastructure/base/k8s/`.

Use ArgoCD, FluxCD ou similar para aplicar os manifests.
