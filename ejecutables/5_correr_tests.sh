#!/bin/bash
echo "====================================================="
echo "  PASO 5: Ejecutando tests automatizados"
echo "====================================================="
pip3 install pytest pytest-cov -q
cd ../tests
python3 -m pytest test_validator.py -v --tb=short
