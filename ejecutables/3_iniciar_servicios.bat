@echo off
echo =====================================================
echo   PASO 3: Iniciando todos los servicios
echo =====================================================
echo.
echo Abriendo cada servicio en su propia ventana...
echo Cierra cada ventana para detener el servicio.
echo.

cd ..\src

:: Error Handler (primero para capturar mensajes desde el inicio)
start "ERROR-HANDLER" cmd /k "python error_handler.py"
timeout /t 2 /nobreak >nul

:: Billing Service (instancia A)
start "BILLING-A" cmd /k "python billing_service.py A"
timeout /t 1 /nobreak >nul

:: Billing Service (instancia B - prueba de Point-to-Point)
start "BILLING-B" cmd /k "python billing_service.py B"
timeout /t 1 /nobreak >nul

:: Notification Service
start "NOTIFICATION" cmd /k "python notification_service.py"
timeout /t 1 /nobreak >nul

:: Analytics Service
start "ANALYTICS" cmd /k "python analytics_service.py"
timeout /t 2 /nobreak >nul

echo.
echo =====================================================
echo  Todos los servicios iniciados.
echo  Ahora ejecuta: 4_enviar_mensajes.bat para probar.
echo =====================================================
pause
