# Generar APK – ¿Quién Quiere Ser Millonario? Bíblico (Kivy)

La app está hecha en **Python + Kivy**. Para obtener el APK se usa **Buildozer**, que solo funciona en **Linux**. En Windows se usa **WSL** (Ubuntu).

---

## Opción rápida (Windows)

1. Instala WSL con Ubuntu si aún no lo tienes (solo una vez):
   ```powershell
   wsl --install -d Ubuntu
   ```
2. Dentro de Ubuntu, instala Buildozer (solo la primera vez). Usa **pipx** (en Ubuntu reciente `pip install --user` da error):
   ```bash
   sudo apt update
   sudo apt install -y pipx python3-venv build-essential openjdk-17-jdk unzip libffi-dev libssl-dev
   pipx ensurepath
   ```
   Cierra y abre la terminal (o `source ~/.bashrc`), luego:
   ```bash
   pipx install buildozer
   ```
3. En el proyecto, **doble clic en `generar_apk.bat`** (o ejecútalo desde la carpeta del proyecto).

El script abre WSL, ejecuta Buildozer y al terminar abre la carpeta `bin\` donde estará el APK.

---

## Opción manual (desde Ubuntu/WSL)

1. Abre **Ubuntu** (WSL).
2. Ve a la carpeta del proyecto:
   ```bash
   cd /mnt/c/Users/Familia/AndroidStudioProjects/millonario_biblico
   ```
3. Genera el APK:
   ```bash
   buildozer android debug
   ```

La primera vez puede tardar **20–40 minutos** (descarga NDK, SDK, compila Python y Kivy). Las siguientes veces será más rápido.

El APK quedará en:
```text
bin/millonariobiblico-1.0-arm64-v8a-debug.apk
```
(o similar con `armeabi-v7a`). Puedes copiarlo al escritorio o a tu móvil.

---

## Si algo falla

- **"buildozer: command not found"**  
  Asegúrate de haber ejecutado `source ~/.bashrc` o de cerrar y abrir Ubuntu después de instalar buildozer, y de que `PATH` incluya `$HOME/.local/bin`.

- **Errores de SDK/NDK**  
  Buildozer los descarga solo. La primera ejecución debe tener internet. Si falla, copia el mensaje de error completo.

- **Poca RAM**  
  En `buildozer.spec` puedes usar una sola arquitectura: `archs = arm64-v8a`.

- **El .bat no encuentra WSL**  
  Asegúrate de tener WSL instalado y de haber abierto al menos una vez Ubuntu para completar la configuración.

---

## Resumen

| Qué quieres        | Cómo                          |
|--------------------|--------------------------------|
| Generar APK rápido | Ejecutar `generar_apk.bat`     |
| Generar APK a mano | En Ubuntu: `buildozer android debug` |
| Dónde está el APK  | Carpeta `bin/` del proyecto    |

El código está en `main.py`, `main.kv`, `screens/`, `config.py` y los recursos en `assets/`, `sounds/`, `preguntas/`.
