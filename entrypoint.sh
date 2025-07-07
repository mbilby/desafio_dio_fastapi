#!/bin/bash
set -e

echo "Aguardando o banco de dados em db:5432..."
# Você precisaria de um script 'wait-for-it.sh' ou similar aqui
# Ou, se você confia no 'depends_on: condition: service_healthy', pode remover esta linha
# /app/wait-for-it.sh db:5432 --timeout=30 -- echo "Banco de dados está pronto!"

echo "Executando migrations do banco de dados..."
PYTHONPATH=/app make run-migrations # Chama o make target para migrations

echo "Iniciando a aplicação Uvicorn..."
exec PYTHONPATH=/app uvicorn api.app:app --host 0.0.0.0 --port 8000