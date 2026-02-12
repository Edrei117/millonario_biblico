# Generar APK desde Ubuntu (máquina virtual)

No hace falta rehacer el proyecto. El código ya es compatible con Linux: usa `os.path` y `BASE_DIR`, así que las rutas se resuelven solas en Ubuntu. Solo necesitas tener la misma carpeta del proyecto disponible dentro de la VM e instalar Buildozer ahí.

---

## 1. ¿Hay que cambiar algo del código?

**No.** Todo está pensado para funcionar en cualquier sistema:

- Rutas: `BASE_DIR = os.path.dirname(os.path.abspath(__file__))` y luego `os.path.join(BASE_DIR, 'assets')`, etc.
- No hay rutas tipo `C:\` ni cosas de Windows.
- `buildozer.spec` y los archivos del proyecto sirven igual en Linux.

Solo hay que **tener la carpeta del proyecto dentro de Ubuntu** (compartida o copiada) y ejecutar Buildozer desde ahí.

---

## 2. Cómo tener el proyecto en Ubuntu (VM)

Elige una forma:

### Opción A: Carpeta compartida (recomendado)

Así trabajas sobre los mismos archivos que en Windows.

- **VirtualBox:** Configuración de la VM → Carpetas compartidas → añadir la carpeta del proyecto (ej. `C:\Users\Familia\AndroidStudioProjects\millonario_biblico`). En Ubuntu suele montarse en `/media/sf_NOMBRE` (el nombre depende de cómo la hayas llamado). A veces hay que añadir tu usuario al grupo `vboxsf`:  
  `sudo usermod -aG vboxsf $USER`  
  y cerrar sesión/reiniciar.
- **VMware:** Carpeta compartida de la VM → misma idea. En Ubuntu suele ser algo como `/mnt/hgfs/millonario_biblico`.

Dentro de Ubuntu:

```bash
cd /media/sf_millonario_biblico
# o, en VMware, por ejemplo:
# cd /mnt/hgfs/millonario_biblico
```

(Usa la ruta que te muestre tu VM en “Carpetas compartidas”.)

### Opción B: Copiar la carpeta una vez

Si prefieres no usar carpetas compartidas:

1. En Windows: comprime la carpeta `millonario_biblico` (ZIP), sin incluir `bin/`, `build/`, `.buildozer/`, `__pycache__/` si quieres que pese menos.
2. Pasa el ZIP a la VM (carpeta compartida, USB, red, etc.).
3. En Ubuntu: descomprime en tu home, por ejemplo:
   ```bash
   cd ~
   unzip millonario_biblico.zip
   cd millonario_biblico
   ```

---

## 3. Arreglar saltos de línea del script (solo si falla)

Si los archivos se crearon o editaron en Windows, el script puede tener saltos de línea CRLF y en Ubuntu dar error del tipo “bad interpreter” o “command not found” al ejecutarlo. Arréglalo una vez:

```bash
dos2unix generar_apk_wsl.sh
```

Si no tienes `dos2unix`:

```bash
sudo apt install dos2unix
dos2unix generar_apk_wsl.sh
```

---

## 4. Instalar Buildozer en Ubuntu (solo la primera vez)

En Ubuntu reciente (22.04+) no uses `pip install --user buildozer` (da error *externally-managed-environment*). Usa **pipx**:

```bash
sudo apt update
sudo apt install -y pipx python3-venv build-essential openjdk-17-jdk unzip libffi-dev libssl-dev
pipx ensurepath
```

Cierra la terminal y ábrela de nuevo (o ejecuta `source ~/.bashrc`). Luego:

```bash
pipx install buildozer
```

Con eso `buildozer` quedará en el PATH. Si ya tenías `$HOME/.local/bin` en el PATH, no hace falta añadir nada más.

---

## 5. Generar el APK

Entra en la carpeta del proyecto y ejecuta el script o Buildozer directamente:

```bash
cd /ruta/donde/esta/millonario_biblico   # la misma que usaste arriba

# Opción 1: usar el script
bash generar_apk_wsl.sh

# Opción 2: comando directo
buildozer android debug
```

La primera vez puede tardar 20–40 minutos (descarga SDK, NDK, compila todo). Las siguientes son más rápidas.

El APK se generará en la carpeta **`bin/`** dentro del proyecto, por ejemplo:

- `bin/millonariobiblico-1.0-arm64-v8a-debug.apk`

---

## 6. Pasar el APK a Windows

- **Si usas carpeta compartida:** la carpeta `bin/` está en la misma ruta compartida; en el Explorador de Windows entra en la carpeta del proyecto y abre `bin` para copiar el `.apk`.
- **Si copiaste el proyecto:** copia el archivo `.apk` desde `bin/` de la VM a Windows por la misma forma que usaste (carpeta compartida, USB, etc.).

---

## Resumen

| Paso | Qué hacer |
|------|-----------|
| 1 | En la VM, tener el proyecto (carpeta compartida o copiada). |
| 2 | Si el script da error raro al ejecutarlo, ejecutar `dos2unix generar_apk_wsl.sh`. |
| 3 | Instalar Buildozer y dependencias (solo una vez). |
| 4 | `cd` a la carpeta del proyecto y ejecutar `bash generar_apk_wsl.sh` o `buildozer android debug`. |
| 5 | Coger el APK de `bin/` y pasarlo a Windows si quieres. |

No hace falta “hacer todo de nuevo”: mismo código, misma estructura; solo se ejecuta Buildozer en Ubuntu en lugar de en Windows/WSL.
