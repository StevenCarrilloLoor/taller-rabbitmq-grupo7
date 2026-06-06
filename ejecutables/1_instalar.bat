@echo off
echo =====================================================
echo   TALLER RABBITMQ - INSTALACION AUTOMATICA (Windows)
echo =====================================================
echo.

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado. Descargalo de https://python.org
    pause
    exit /b 1
)
echo [OK] Python encontrado.

:: Verificar pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip no esta instalado.
    pause
    exit /b 1
)
echo [OK] pip encontrado.

:: Verificar Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no esta instalado. Descargalo de https://docker.com
    pause
    exit /b 1
)
echo [OK] Docker encontrado.

:: Verificar Docker Compose
docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose no encontrado. Asegurate de tener Docker Desktop actualizado.
    pause
    exit /b 1
)
echo [OK] Docker Compose encontrado.

:: Instalar dependencias Python
echo.
echo [INFO] Instalando dependencias Python...
pip install -r ..\requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Fallo la instalacion de dependencias.
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas correctamente.

echo.
echo =====================================================
echo  Instalacion completada exitosamente.
echo  Ahora ejecuta: 2_levantar_rabbitmq.bat
echo =====================================================
pause
