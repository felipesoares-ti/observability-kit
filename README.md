# Observability Kit

Este projeto demonstra uma stack de observabilidade local com métricas, logs e traces usando FastAPI, OpenTelemetry, Prometheus, Grafana, Loki, Tempo e Kind.

## Como rodar o projeto

### Pré-requisitos
- Docker
- Kind
- kubectl
- Helm
- Python 3.10+

### Passos principais

```bash
# Crie o cluster local
make cluster

# Instale os componentes de observabilidade
yarn install # se necessário para dependências JS
make deploy

# Rode localmente (apenas FastAPI)
cd app
python -m venv .venv && .venv/Scripts/activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Exemplos de uso

```bash
curl http://localhost:8000/ping
curl http://localhost:8000/metrics
curl http://localhost:8000/healthz
```

### Troubleshooting
- Verifique variáveis de ambiente (exemplo em `.env.example`).
- Certifique-se de que as portas não estão em uso.
- Logs detalhados são exibidos no console.

## Scripts do Makefile

- `make cluster`: Cria o cluster local Kind.
- `make deploy`: Faz o deploy de todos os componentes (aplicação, otel-collector, Prometheus, Grafana, Loki, Tempo).
- `make destroy`: Remove o cluster Kind.
- `make logs`: Exibe os logs do app.

## Testes

1. Instale as dependências de desenvolvimento:
   ```bash
   pip install -r app/requirements-dev.txt
   ```
2. Execute os testes:
   ```bash
   pytest tests/
   ```
3. Para cobertura:
   ```bash
   pytest --cov=app tests/
   ```

## Lint e formatação

- Para checar formatação e importação:
  ```bash
  black --check app/
  isort --check-only app/
  ```
- Para corrigir automaticamente:
  ```bash
  black app/
  isort app/
  ```

## Segurança
- Use o arquivo `.env.example` como base para criar seu `.env` com variáveis sensíveis.
- O `.env` já está no `.gitignore`.

## Estrutura
- `app/`: aplicação Python instrumentada
- `infrastructure/`: infraestrutura GitOps, manifests, overlays e charts customizados
- `Makefile`: automação
- `tests/`: testes automatizados

## CI/CD

Sugestão: utilize GitHub Actions ou GitLab CI para rodar testes e lint automaticamente. Exemplo de workflow para GitHub Actions:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r app/requirements.txt
          pip install -r app/requirements-dev.txt
      - name: Lint
        run: |
          black --check app/
          isort --check-only app/
      - name: Test
        run: pytest tests/
```
