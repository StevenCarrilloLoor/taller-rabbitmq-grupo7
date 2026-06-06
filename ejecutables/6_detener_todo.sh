#!/bin/bash
echo "[INFO] Deteniendo servicios Python..."
for pid_file in /tmp/rabbitmq-taller-pids/*.pid; do
    kill $(cat "$pid_file") 2>/dev/null
done
rm -rf /tmp/rabbitmq-taller-pids
echo "[INFO] Deteniendo RabbitMQ Docker..."
cd ..
docker compose down
echo "[OK] Todo detenido."
