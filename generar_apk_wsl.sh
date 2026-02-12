#!/bin/bash
# Script para generar el APK de la app Kivy (Python) desde WSL.
# Uso: en Ubuntu (WSL), desde esta carpeta: bash generar_apk_wsl.sh

set -e
cd "$(dirname "$0")"

echo "=== Millonario Biblico - Generar APK (Kivy/Buildozer) ==="
echo "Carpeta: $(pwd)"
echo ""

if ! command -v buildozer &> /dev/null; then
    echo "Buildozer no esta instalado."
    echo "En Ubuntu reciente usa pipx (evita el error externally-managed-environment):"
    echo "  sudo apt update"
    echo "  sudo apt install -y pipx python3-venv build-essential openjdk-17-jdk unzip libffi-dev libssl-dev"
    echo "  pipx ensurepath"
    echo "  (cierra y abre la terminal, luego)"
    echo "  pipx install buildozer"
    exit 1
fi

echo "Ejecutando: buildozer android debug"
echo "(La primera vez puede tardar 20-40 minutos.)"
echo ""
buildozer android debug

echo ""
echo "=== APK generado ==="
if [ -d "bin" ]; then
    ls -la bin/*.apk 2>/dev/null || true
    echo "Copia el .apk de la carpeta bin/ a tu telefono o escritorio."
else
    echo "Revisa si hubo errores arriba."
fi
