# Ejecutar la app en Ubuntu (desde Cursor o terminal)

## 1. Dependencias (solo la primera vez)

Si el proyecto está en una **carpeta compartida** (p. ej. `/media/sf_millonario_biblico`), no se puede crear el venv ahí. Créalo en tu home:

```bash
python3 -m venv ~/venv_millonario_biblico
source ~/venv_millonario_biblico/bin/activate
cd /media/sf_millonario_biblico   # o la ruta de tu proyecto
pip install -r requirements.txt
```

Si el proyecto **no** está en carpeta compartida, puedes usar un venv dentro del proyecto:

```bash
cd /ruta/a/millonario_biblico
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. En Linux siempre usa main_linux.py (no main.py)

En Linux/Ubuntu/VirtualBox se usa **main_linux.py**. Por defecto **no carga audio** para que la app no se quede pegada; el juego funciona normal pero sin sonidos. **main.py** queda solo para Windows.

### Forma recomendada: script que fuerza X11

```bash
cd /media/sf_millonario_biblico
chmod +x run_app.sh
./run_app.sh
```

El script ejecuta **main_linux.py** y usa el venv de tu home si existe (`~/venv_millonario_biblico`). La app debería completar la carga y llegar al menú sin bloquearse.

### Si quieres intentar con audio en Linux

Ejecuta desde una copia local (evita carpeta compartida) y activa audio:

```bash
./run_app_local.sh
# Luego en otra terminal o edita run_app_local.sh para añadir:
KIVY_SKIP_AUDIO=0 python3 main_linux.py
```

O desde la copia: `cd ~/millonario_biblico_run && KIVY_SKIP_AUDIO=0 python3 main_linux.py`. Si aun así se pega, en Linux se usa sin audio.

## 3. Desde Cursor (Linux)

- **Ctrl+Shift+P** → "Python: Select Interpreter" → el que apunte a `~/venv_millonario_biblico/bin/python`.
- **F5** o **Run → Start Debugging** → elige **"Millonario Bíblico (Linux)"** (usa main_linux.py).

## 4. Desde la terminal (sin script)

```bash
cd /media/sf_millonario_biblico
source ~/venv_millonario_biblico/bin/activate
python3 main_linux.py
```

Para forzar X11 a mano:

```bash
SDL_VIDEODRIVER=x11 GDK_BACKEND=x11 python3 main.py
```

## 5. Error del portapapeles (xclip / Cutbuffer)

Si ves `[CRITICAL] [Cutbuffer] Unable to find any valuable Cutbuffer provider` o `'xclip': No such file or directory`:

```bash
sudo apt install xclip
```

Opcional: `sudo apt install xsel`. La app puede funcionar sin ellos, pero instalarlos quita el aviso.

## 6. Si se cuelga o sale "Killed" en la pantalla de carga (44%…)

La app ya carga preguntas y sonidos en hilos en segundo plano para no bloquear. Si aun así se mata el proceso:

- Prueba **sin cargar audio** (para comprobar que es el audio):  
  `KIVY_SKIP_AUDIO=1 ./run_app.sh`  
  Si así termina la carga y llega al menú, el problema era la carga de sonidos; en ese caso usa `./run_app_local.sh` (ejecuta desde una copia en tu home).

## 7. Si sigue fallando (ventana en blanco, "not responding" o "Killed")

1. **Ejecutar desde copia en tu home** (recomendado en VirtualBox con carpeta compartida):
   ```bash
   chmod +x run_app_local.sh
   ./run_app_local.sh
   ```
   El script copia el proyecto a `~/millonario_biblico_run` y ejecuta desde ahí (todo el I/O es local; evita que el proceso sea "Killed" por lentitud de la carpeta compartida). Necesitas `rsync`: `sudo apt install rsync`.

2. **Sesión X11:** Cierra sesión, en el login elige **"Ubuntu on Xorg"** en lugar de Wayland e inicia sesión. Luego ejecuta `./run_app.sh` de nuevo.

3. **VirtualBox:** Configuración de la VM → Pantalla → activa **Aceleración 2D** y prueba con/sin **Aceleración 3D**.

---

**Resumen:** Primero `./run_app.sh`. Si la ventana se queda en blanco o sale "Killed", usa `./run_app_local.sh`. Instala `xclip` para quitar el aviso del portapapeles.
