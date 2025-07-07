# Makefile

run:
	@uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload

create-migrations:
	@PYTHONPATH=$(PYTHONPATH):$(pwd) alembic revision --autogenerate -m $(d)

run-migrations:
	@PYTHONPATH=$(PYTHONPATH):$(pwd) alembic upgrade head

docker-run: run-migrations
	@echo "Migrations aplicadas. Iniciando a aplicação Uvicorn..."
	sh -c "exec uvicorn api.app:app --host 0.0.0.0 --port 8000"