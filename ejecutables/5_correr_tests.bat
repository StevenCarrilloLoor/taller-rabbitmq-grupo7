@echo off
echo =====================================================
echo   PASO 5: Ejecutando tests automatizados
echo =====================================================
echo.
pip install pytest pytest-cov >nul 2>&1
cd ..\tests
pytest test_validator.py -v --tb=short
echo.
pause
