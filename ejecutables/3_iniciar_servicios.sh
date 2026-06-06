#!/bin/bash
echo "====================================================="
echo "  PASO 3: Iniciando todos los servicios"
echo "====================================================="
echo

cd ../src

# Guardar PIDs para poder detenerlos
mkdir -p /tmp/rabbitmq-taller-pids

echo "[INFO] Iniciando error-handler..."
python3 error_handler.py > /tmp/rabbitmq-taller-error.log 2>&1 &
echo $! > /tmp/rabbitmq-taller-pids/error_handler.pid
sleep 1

echo "[INFO] Iniciando billing-service (instancia A)..."
python3 billing_service.py A > /tmp/rabbitmq-taller-billing-a.log 2>&1 &
echo $! > /tmp/rabbitmq-taller-pids/billing_a.pid
sleep 1

echo "[INFO] Iniciando billing-service (instancia B - Point-to-Point test)..."
python3 billing_service.py B > /tmp/rabbitmq-taller-billing-b.log 2>&1 &
echo $! > /tmp/rabbitmq-taller-pids/billing_b.pid
sleep 1

echo "[INFO] Iniciando notification-service..."
python3 notification_service.py > /tmp/rabbitmq-taller-notification.log 2>&1 &
echo $! > /tmp/rabbitmq-taller-pids/notification.pid
sleep 1

echo "[INFO] Iniciando analytics-service..."
python3 analytics_service.py > /tmp/rabbitmq-taller-analytics.log 2>&1 &
echo $! > /tmp/rabbitmq-taller-pids/analytics.pid
sleep 2

echo
echo "====================================================="
echo " Todos los servicios iniciados en background."
echo " Logs disponibles en /tmp/rabbitmq-taller-*.log"
echo " Ejecuta: bash 4_enviar_mensajes.sh para probar."
echo " Para ver logs: tail -f /tmp/rabbitmq-taller-billing-a.log"
echo "====================================================="
