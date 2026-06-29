# desafio_dio_fastapi

API assíncrona em FastAPI para gerenciar atletas, categorias e centros de treinamento.

## Visao geral

O projeto organiza uma API REST com FastAPI, SQLAlchemy assíncrono, Alembic e PostgreSQL.
O ponto de entrada fica em `api/app.py` e o roteamento principal em `api/routers/routers.py`.

## O que esta na aplicacao

- Cadastro, consulta, alteração e remoção de atletas.
- Cadastro e consulta de categorias.
- Cadastro e consulta de centros de treinamento.
- Banco configurado por `DB_URL` via arquivo `.env`.
- Execução local e em Docker.

## Estrutura

```mermaid
graph TD
  A[Cliente] --> B[FastAPI app]
  B --> C[Roteadores]
  C --> D[Atletas]
  C --> E[Categorias]
  C --> F[Centros de treinamento]
  D --> G[SQLAlchemy async]
  E --> G
  F --> G
  G --> H[PostgreSQL]
```

## Rotas principais

| Recurso | Rotas | Finalidade |
| --- | --- | --- |
| Atletas | `POST /v1/atletas/` `GET /v1/atletas/` `GET /v1/atletas/atleta` `PATCH /v1/atletas/{id}` `DELETE /v1/atletas/{id}` | Criar, listar, buscar, atualizar e remover atletas |
| Categorias | `POST /v1/categorias/` `GET /v1/categorias/` `GET /v1/categorias/{id}` | Criar e consultar categorias |
| Centros de treinamento | `POST /v1/centros-treinamento/` `GET /v1/centros-treinamento/` `GET /v1/centros-treinamento/{id}` | Criar e consultar centros de treinamento |

## Requisitos

- Python 3.11 ou superior.
- PostgreSQL.
- `DB_URL` definido no ambiente ou em `.env`.

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DB_URL="postgresql+asyncpg://workout:workout@localhost:5432/workout"
make run-migrations
make run
```

## Como rodar com Docker

```bash
docker compose up --build
```

O `docker-compose.yml` sobe um banco PostgreSQL e a aplicacao lendo as variaveis de `env_file`.

## Comandos uteis

```bash
make create-migrations d="nome_da_migracao"
make run-migrations
make run
```

## Pontos de interesse no codigo

- `api/app.py` define a aplicacao FastAPI.
- `api/routers/routers.py` agrega as rotas da API.
- `api/configs/settings.py` carrega configuracao de ambiente.
- `api/configs/database.py` cria a engine e a session async.
- `alembic/` guarda as migracoes.

## Observacao

Os endpoints usam prefixo `/v1` e o FastAPI expoe a documentacao padrao em `/docs` e `/redoc`.
