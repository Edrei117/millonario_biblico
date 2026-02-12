#!/usr/bin/env bash
# Copia el proyecto a tu home y ejecuta desde ahí (evita "Killed" por carpeta compartida lenta)
# Usar cuando ./run_app.sh deja la ventana en blanco o el proceso termina con "Killed"
set -e
ORIGEN="$(cd "$(dirname "$0")" && pwd)"
DESTINO="$HOME/millonario_biblico_run"
export SDL_VIDEODRIVER=x11
export GDK_BACKEND=x11

if ! command -v rsync >/dev/null 2>&1; then
    echo "Instala rsync: sudo apt install rsync"
    exit 1
fi
echo "[Millonario] Copiando proyecto a $DESTINO ..."
mkdir -p "$DESTINO"
rsync -a --exclude=".venv" --exclude="venv" --exclude="__pycache__" --exclude=".git" \
    "$ORIGEN/" "$DESTINO/"
cd "$DESTINO"
# En Linux usar main_linux.py (carga en hilos)
if [ -x "$HOME/venv_millonario_biblico/bin/python3" ]; then
    exec "$HOME/venv_millonario_biblico/bin/python3" main_linux.py "$@"
else
    exec python3 main_linux.py "$@"
fi
