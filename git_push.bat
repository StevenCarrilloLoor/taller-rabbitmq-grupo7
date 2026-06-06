@echo off
echo ================================================
echo  Subiendo proyecto a GitHub...
echo ================================================
cd /d "C:\Users\steve\AppData\Roaming\Claude\local-agent-mode-sessions\0040b880-86f7-4d8d-9c2e-21c89b9193d5\ee196b89-eb28-4aeb-8c03-78f94c796618\local_3629c06f-0cb4-4798-a137-8514570ddcda\outputs\rabbitmq-taller"
git init
git config user.email "stevencarrilloloor@gmail.com"
git config user.name "StevenCarrilloLoor"
git add .
git commit -m "Semana 8: Taller Patrones de Mensajeria con RabbitMQ - Grupo 7"
git branch -M main
git remote add origin https://github.com/StevenCarrilloLoor/taller-rabbitmq-grupo7.git
git push -u origin main
echo.
echo ================================================
echo  Proyecto subido exitosamente.
echo  URL: https://github.com/StevenCarrilloLoor/taller-rabbitmq-grupo7
echo ================================================
pause
