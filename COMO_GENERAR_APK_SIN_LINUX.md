# Generar el APK sin usar Linux (GitHub Actions)

Puedes generar el APK **en la nube** desde Windows, sin WSL, sin VM ni Ubuntu. Solo necesitas una cuenta de GitHub y subir el proyecto.

---

## Pasos

### 1. Crear un repositorio en GitHub

1. Entra en **https://github.com** e inicia sesión.
2. Clic en **"New"** (nuevo repositorio).
3. Ponle un nombre (ej. `millonario_biblico`) y crea el repo (puedes dejarlo público o privado).
4. **No** marques "Add a README" si ya tienes el proyecto en tu PC.

### 2. Subir el proyecto desde Windows

Abre **PowerShell** o **Símbolo del sistema** en la carpeta del proyecto (`millonario_biblico`):

```powershell
cd C:\Users\Familia\AndroidStudioProjects\millonario_biblico

git init
git add .
git commit -m "Proyecto Millonario Bíblico Kivy"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/millonario_biblico.git
git push -u origin main
```

(Sustituye `TU_USUARIO` por tu usuario de GitHub. Si GitHub te pide usuario/contraseña, usa un **Personal Access Token** en lugar de la contraseña, o configura Git con SSH.)

Si ya tienes Git y el repo creado, basta con:

```powershell
git add .
git commit -m "Actualizar proyecto"
git push
```

### 3. Generar el APK en GitHub

1. En GitHub, abre tu repositorio.
2. Arriba, ve a la pestaña **"Actions"**.
3. En el menú de la izquierda elige **"Build APK (Kivy)"**.
4. Clic en **"Run workflow"** (botón derecho) y luego en **"Run workflow"** verde.
5. Espera a que termine el trabajo (la **primera vez** puede tardar 30–50 minutos; descarga SDK, NDK, etc.). Las siguientes serán más rápidas si GitHub reutiliza la caché.

### 4. Descargar el APK

1. Cuando el workflow termine en verde (✓), entra en la última ejecución.
2. Abajo de la página, en **"Artifacts"**, aparecerá **"apk-millonario-biblico"**.
3. Clic en ese nombre para **descargar un ZIP** con el/los APK.
4. Descomprime el ZIP y tendrás el archivo `.apk` para instalar en el móvil o compartir.

---

## Resumen

| Qué hacer              | Dónde / Cómo                                      |
|------------------------|----------------------------------------------------|
| Subir código           | `git push` desde la carpeta del proyecto           |
| Lanzar la compilación  | GitHub → Actions → Build APK (Kivy) → Run workflow  |
| Descargar el APK       | Misma ejecución → Artifacts → apk-millonario-biblico |

No necesitas Linux, WSL ni VM en tu PC: todo se ejecuta en los servidores de GitHub.

---

## Si no usas Git todavía

1. Instala Git para Windows: **https://git-scm.com/download/win**
2. Crea la cuenta en **https://github.com** si no la tienes.
3. Sigue los pasos de arriba desde el paso 1.

## Si el workflow falla

- Revisa la pestaña **Actions** → la ejecución fallida → el **job** en rojo para ver el log.
- Asegúrate de que en el repo están `main.py`, `main.kv`, `buildozer.spec`, las carpetas `screens/`, `assets/`, `sounds/`, `preguntas/`, etc. (el `.gitignore` evita subir `venv`, `bin`, `.buildozer`).
- Si quieres acelerar la compilación, en `buildozer.spec` puedes dejar solo una arquitectura: `archs = arm64-v8a`.
