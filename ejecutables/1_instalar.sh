#!/bin/bash
echo "====================================================="
echo "  TALLER RABBITMQ - INSTALACION AUTOMATICA (Linux/Mac)"
echo "====================================================="
echo

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 no esta instalado. Instálalo con tu gestor de paquetes."
    exit 1
fi
echo "[OK] Python3 encontrado: $(python3 --version)"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker no esta instalado. Descargalo de https://docker.com"
    exit 1
fi
echo "[OK] Docker encontrado: $(docker --version)"

# Verificar Docker Compose
if ! docker compose version &> /dev/null; then
    echo "[ERROR] Docker Compose no encontrado."
    exit 1
fi
echo "[OK] Docker Compose encontrado."

# Instalar dependencias Python
echo
echo "[INFO] Instalando dependencias Python..."
pip3 install -r ../requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Fallo la instalacion de dependencias."
    exit 1
fi
echo "[OK] Dependencias instaladas."

echo
echo "====================================================="
echo " Instalacion completada."
echo " Ahora ejecuta: bash 2_levantar_rabbitmq.sh"
echo "====================================================="
