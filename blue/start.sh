#!/bin/sh
cd /app/backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 &
cd /
python3 -m http.server 3000 --directory /var/www/html &
wait
