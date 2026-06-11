#!/bin/sh

ACTUAL="blue"
echo "[INICIO] Tráfico inicial → blue"

while true; do
  sleep 7

  if [ "$ACTUAL" = "blue" ]; then
    ACTUAL="green"
  else
    ACTUAL="blue"
  fi

  echo "[$(date)] Cambiando tráfico a: $ACTUAL"

  cat > /etc/nginx/nginx.conf << NGINX
events {
    worker_connections 1024;
}

http {
    upstream produccion_frontend {
        server ${ACTUAL}:3000;
    }

    upstream produccion_api {
        server ${ACTUAL}:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location ~* ^/(auth|productos|ordenes|chat|faq|perfiles|static)(\/|\$) {
            proxy_pass http://produccion_api;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        location / {
            proxy_pass http://produccion_frontend;
            proxy_set_header Host \$host;
            add_header X-Ambiente "${ACTUAL}" always;
        }
    }
}
NGINX

  nginx -s reload
  echo "[$(date)] Nginx recargado → $ACTUAL activo"
done
