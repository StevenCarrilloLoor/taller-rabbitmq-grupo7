@echo off
echo ============================================
echo  Push completo a GitHub
echo ============================================
cd /d "%~dp0"

echo Inicializando git...
git init
git remote remove origin 2>nul
git remote add origin https://github.com/StevenCarrilloLoor/taller-rabbitmq-grupo7.git

echo Configurando branch...
git checkout -b main 2>nul || git checkout main

echo Agregando todos los archivos...
git add -A

echo Haciendo commit...
git commit -m "Add complete project: src, tests, ejecutables, camel routes"

echo Haciendo push (force para sincronizar con repo existente)...
git push -u origin main --force

echo [OK] Push completado.
pause
