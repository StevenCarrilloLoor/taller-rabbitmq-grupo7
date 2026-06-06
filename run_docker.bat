@echo off
echo ================================================
echo  Levantando RabbitMQ + Servicios
echo ================================================
cd /d "C:\Users\steve\AppData\Roaming\Claude\local-agent-mode-sessions\0040b880-86f7-4d8d-9c2e-21c89b9193d5\ee196b89-eb28-4aeb-8c03-78f94c796618\local_3629c06f-0cb4-4798-a137-8514570ddcda\outputs\rabbitmq-taller"
docker compose up -d
echo [INFO] Esperando 20 segundos...
timeout /t 20 /nobreak
cd src
python setup_rabbitmq.py
echo.
echo [INFO] Iniciando servicios en ventanas separadas...
start "ERROR-HANDLER" cmd /k "cd /d C:\Users\steve\AppData\Roaming\Claude\local-agent-mode-sessions\0040b880-86f7-4d8d-9c2e-21c89b9193d5\ee196b89-eb28-4aeb-8c03-78f94c796618\local_3629c06f-0cb4-4798-a137-8514570ddcda\outputs\rabbitmq-taller\src && python error_handler.py"
timeout /t 2 /nobreak
start "BILLING-A" cmd /k "cd /d C:\Users\steve\AppData\Roaming\Claude\local-agent-mode-sessions\0040b880-86f7-4d8d-9c2e-21c89b9193d5\ee196b89-eb28-4aeb-8c03-78f94c796618\local_3629c06f-0cb4-4798-a137-8514570ddcda\outputs\rabbitmq-taller\src && python billing_service.py A"
timeout /t 1 /nobreak
start "BILLING-B" cmd /k "cd /d C:\Users\steve\AppData\Roaming\Claude\local-agent-mode-sessions\0040b880-86f7-4d8d-9c2e-21c89b9193d5\ee196b89-eb28-4aeb-8c03-78f94c796618\local_3629c06f-0cb4-4798-a137-8514570ddcda\outputs\rabbitmq-taller\src && python billing_service.py B"
timeout /t 1 /nobreak
start "NOTIFICATION" cmd /k "cd /d C:\Users\steve\AppData\Roaming\Claude\local-agent-mode-sessions\0040b880-86f7-4d8d-9c2e-21c89b9193d5\ee196b89-eb28-4aeb-8c03-78f94c796618\local_3629c06f-0cb4-4798-a137-8514570ddcda\outputs\rabbitmq-taller\src && python notification_service.py"
timeout /t 1 /nobreak
start "ANALYTICS" cmd /k "cd /d C:\Users\steve\AppData\Roaming\Claude\local-agent-mode-sessions\0040b880-86f7-4d8d-9c2e-21c89b9193d5\ee196b89-eb28-4aeb-8c03-78f94c796618\local_3629c06f-0cb4-4798-a137-8514570ddcda\outputs\rabbitmq-taller\src && python analytics_service.py"
timeout /t 3 /nobreak
echo.
echo [INFO] Enviando mensajes de prueba...
python orders_producer.py
echo ================================================
echo  Listo. Abre http://localhost:15672 (admin/admin123)
echo ================================================
pause
