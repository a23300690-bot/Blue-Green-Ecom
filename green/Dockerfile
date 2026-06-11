FROM python:3.11-slim

RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

COPY frontend/ /var/www/html/

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000 3000

CMD ["/start.sh"]
