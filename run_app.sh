#!/usr/bin/env bash
# Ejecuta Millonario Bíblico forzando X11 (recomendado en Ubuntu con Wayland / VirtualBox)
cd "$(dirname "$0")"
export SDL_VIDEODRIVER=x11
export GDK_BACKEND=x11
# Evitar error de portapapeles (Cutbuffer) si no tienes xclip: sudo apt install xclip
if ! command -v xclip >/dev/null 2>&1; then
    echo "[Aviso] Instala xclip para evitar un aviso del portapapeles: sudo apt install xclip"
fi
# En Linux usar main_linux.py (carga en hilos, evita bloqueos). Windows usa main.py
if [ -x "$HOME/venv_millonario_biblico/bin/python3" ]; then
    exec "$HOME/venv_millonario_biblico/bin/python3" main_linux.py "$@"
else
    exec python3 main_linux.py "$@"
fi
