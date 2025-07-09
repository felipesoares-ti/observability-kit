Cada pasta representa um chart Helm customizado. Coloque o values.yaml correspondente dentro de cada uma (grafana, loki, prometheus, tracing-backend).

- O diretório `helm/` na raiz foi removido. Utilize apenas `infrastructure/helm/` para charts customizados.
- Os manifests do Kubernetes estão centralizados em `infrastructure/base/k8s/`.

- grafana/values.yaml
- loki/values.yaml
- prometheus/values.yaml
- tracing-backend/values.yaml
