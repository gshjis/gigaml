# Этап сборки с установкой системных зависимостей
FROM python:3.12-slim as builder

# Установка системных зависимостей для pygraphviz и сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    libgraphviz-dev \
    pkg-config \
    make \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Установка Python-зависимостей с явным указанием путей для pygraphviz
RUN pip install --upgrade pip && \
    pip install pygraphviz --global-option=build_ext \
                          --global-option="-I/usr/include/graphviz" \
                          --global-option="-L/usr/lib/graphviz" && \
    pip install -r requirements.txt

# Финальный образ
FROM python:3.12-slim

# Установка только runtime-зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем только необходимое из builder-этапа
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

CMD ["make", "run_docker_server"]