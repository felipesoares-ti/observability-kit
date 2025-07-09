# Testes do Projeto Observability Kit

Este diretório contém os testes automatizados do projeto.

## Como rodar os testes

1. Certifique-se de que as dependências de desenvolvimento estão instaladas:

   ```bash
   pip install -r app/requirements-dev.txt
   ```

2. Execute os testes com:

   ```bash
   pytest tests/
   ```

3. Para verificar cobertura de testes:

   ```bash
   pytest --cov=app tests/
   ```

Inclua novos testes para garantir a qualidade e robustez do projeto.
