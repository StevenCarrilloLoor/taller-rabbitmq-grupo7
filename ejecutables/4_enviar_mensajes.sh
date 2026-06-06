#!/bin/bash
echo "====================================================="
echo "  PASO 4: Enviando mensajes de prueba"
echo "====================================================="
cd ../src
python3 orders_producer.py
echo
echo "====================================================="
echo " Logs de servicios:"
echo "   tail -f /tmp/rabbitmq-taller-billing-a.log"
echo "   tail -f /tmp/rabbitmq-taller-notification.log"
echo "   tail -f /tmp/rabbitmq-taller-analytics.log"
echo "   tail -f /tmp/rabbitmq-taller-error.log"
echo "====================================================="
