@echo off
echo =====================================================
echo   PASO 2: Levantando RabbitMQ con Docker Compose
echo =====================================================
echo.

cd ..
docker compose up -d

if %errorlevel% neq 0 (
    echo [ERROR] No se pudo levantar RabbitMQ. Asegurate de que Docker este corriendo.
    pause
    exit /b 1
)

echo.
echo [INFO] Esperando que RabbitMQ arranque (15 segundos)...
timeout /t 15 /nobreak >nul

echo.
echo [INFO] Configurando exchanges y queues...
cd src
python setup_rabbitmq.py
cd ..

if %errorlevel% neq 0 (
    echo [ERROR] Fallo la configuracion de RabbitMQ.
    pause
    exit /b 1
)

echo.
echo =====================================================
echo  RabbitMQ levantado y configurado.
echo  Management UI: http://localhost:15672
echo  Usuario: admin  /  Contrasena: admin123
echo  Ahora ejecuta: 3_iniciar_servicios.bat
echo =====================================================
pause
