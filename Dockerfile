FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt

COPY . .

# Команда для запуска приложения
CMD ["make", "run_docker_server"]
