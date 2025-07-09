.PHONY: cluster deploy destroy logs

cluster:
	kind create cluster --name obs-cluster

deploy:
	kubectl apply -f k8s/namespace-monitoring.yaml
	kubectl apply -f k8s/deployments/app-deployment.yaml
	kubectl apply -f k8s/services/app-service.yaml
	kubectl apply -f k8s/deployments/otel-collector-deployment.yaml
	kubectl apply -f k8s/services/otel-collector-service.yaml
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo update
	helm upgrade --install prometheus prometheus-community/prometheus --namespace monitoring
	helm upgrade --install grafana grafana/grafana --namespace monitoring --set adminPassword=prom-operator --wait
	helm upgrade --install loki grafana/loki-stack --namespace monitoring --set grafana.enabled=false --wait
	helm upgrade --install tracing-backend grafana/tempo --namespace monitoring --wait

destroy:
	kind delete cluster --name obs-cluster

logs:
	kubectl logs -l app=observability-app -f
