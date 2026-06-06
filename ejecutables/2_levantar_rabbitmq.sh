#!/bin/bash
echo "====================================================="
echo "  PASO 2: Levantando RabbitMQ con Docker Compose"
echo "====================================================="
echo

cd ..
docker compose up -d

if [ $? -ne 0 ]; then
    echo "[ERROR] No se pudo levantar RabbitMQ. Asegurate de que Docker este corriendo."
    exit 1
fi

echo
echo "[INFO] Esperando que RabbitMQ arranque (15 segundos)..."
sleep 15

echo "[INFO] Configurando exchanges y queues..."
cd src
python3 setup_rabbitmq.py
cd ..

if [ $? -ne 0 ]; then
    echo "[ERROR] Fallo la configuracion de RabbitMQ."
    exit 1
fi

echo
echo "====================================================="
echo " RabbitMQ levantado y configurado."
echo " Management UI: http://localhost:15672"
echo " Usuario: admin  /  Contraseña: admin123"
echo " Ahora ejecuta: bash 3_iniciar_servicios.sh"
echo "====================================================="
