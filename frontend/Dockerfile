FROM nginx:alpine

# Кеширование статических ресурсов
COPY . /usr/share/nginx/html

# Настройка nginx для SPA
RUN echo ' \
    server { \
    listen 80; \
    root /usr/share/nginx/html; \
    \
    location / { \
    try_files $uri $uri/ /index.html; \
    } \
    \
    location /api { \
    proxy_pass http://backend:8000; \
    } \
    } \
    ' > /etc/nginx/conf.d/default.conf

EXPOSE 80
