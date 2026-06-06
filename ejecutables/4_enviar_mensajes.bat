@echo off
echo =====================================================
echo   PASO 4: Enviando mensajes de prueba
echo =====================================================
echo.
cd ..\src
python orders_producer.py
echo.
echo =====================================================
echo  Mensajes enviados. Revisa las ventanas de los 
echo  servicios para ver el procesamiento.
echo =====================================================
pause
