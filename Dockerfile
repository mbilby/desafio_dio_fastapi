# Use uma imagem oficial do Python como base
FROM python:3.13.4-alpine3.22

# Define o diretório de trabalho dentro do container
WORKDIR /app

RUN apk update && apk add --no-cache \
    make \
    build-base \
    # Adicione outras dependências que seu app precise (ex: postgresql-dev para psycopg2)
    # && rm -rf /var/lib/apk/lists/* # No alpine, o --no-cache já cuida disso
    && rm -rf /var/cache/apk/* # Limpa o cache para reduzir o tamanho da imagem

# Copia os arquivos de requisitos, se existirem
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o entrypoint para o container
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY Makefile .

COPY . /app

# Define PYTHONPATH globalmente
ENV PYTHONPATH=/app

# Comando para iniciar a aplicação
CMD ["make", "docker-run"]

EXPOSE 8000