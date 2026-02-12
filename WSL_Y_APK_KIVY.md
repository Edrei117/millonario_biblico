# Si "wsl" no se reconoce: activar WSL y generar el APK Kivy

Cuando PowerShell dice **"El término 'wsl' no se reconoce"**, significa que Windows Subsystem for Linux (WSL) no está instalado o no está activado. Sigue estos pasos.

---

## Requisitos de Windows

- **Windows 10** versión 2004 o superior (Build 19041 o mayor), o **Windows 11**.
- Para ver tu versión: **Configuración → Sistema → Acerca de** (o escribe `winver` en Inicio).

Si tienes una versión antigua de Windows 10, actualiza primero.

---

## Opción A: Activar WSL desde Características de Windows

1. Pulsa **Win + R**, escribe **`optionalfeatures`** y Enter.
2. Se abre **"Activar o desactivar las características de Windows"**.
3. Busca en la lista:
   - **Subsistema de Windows para Linux**
   - (En inglés: **Windows Subsystem for Linux**)
4. **Marca la casilla** y pulsa **Aceptar**.
5. Cuando pida **reiniciar**, reinicia el PC.
6. Después del reinicio, abre **PowerShell como administrador** y ejecuta:
   ```powershell
   wsl --install -d Ubuntu
   ```
   Si ahora sí reconoce `wsl`, descargará Ubuntu. Cuando termine, reinicia si te lo pide.
7. Abre **Ubuntu** desde el menú Inicio, crea usuario y contraseña la primera vez.
8. Sigue la guía **COMO_GENERAR_APK_KIVY.md**: entra a la carpeta del proyecto en WSL e instala Buildozer, luego `buildozer android debug`.

---

## Opción B: Actualizar WSL (si ya tenías "Subsistema para Linux" antiguo)

En algunas instalaciones antiguas el comando es **`wsl.exe`** o solo funciona tras una actualización:

1. Abre **Microsoft Store**.
2. Busca **"Windows Subsystem for Linux"** o **"WSL"**.
3. Instala o actualiza la aplicación que aparezca.
4. Reinicia y en **PowerShell (Administrador)** prueba de nuevo:
   ```powershell
   wsl --install -d Ubuntu
   ```

---

## Opción C: No usar WSL – generar APK en la nube (GitHub Actions)

Si no puedes o no quieres usar WSL, puedes generar el APK **sin Linux en tu PC** usando GitHub Actions. Ver **COMO_GENERAR_APK_SIN_LINUX.md**.
