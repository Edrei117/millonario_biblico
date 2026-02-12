# Instalar WSL en Windows (sin usar comandos que falle)

Si en PowerShell no se reconocen `wsl` ni `dism.exe`, hazlo todo por **menús de Windows** y **Microsoft Store**.

---

## Método 1: Activar WSL por la interfaz de Windows (recomendado)

Así no necesitas escribir ningún comando.

1. Pulsa **Win + R** (tecla Windows y R a la vez) para abrir "Ejecutar".
2. Escribe:
   ```text
   optionalfeatures
   ```
   y pulsa **Aceptar**.
3. Se abrirá **"Activar o desactivar las características de Windows"**.
4. En la lista, busca y **marca** estas dos casillas:
   - **Subsistema de Windows para Linux**
   - **Plataforma de máquina virtual**
5. Pulsa **Aceptar**. Si pide reiniciar, **reinicia el PC**.
6. Después del reinicio, abre **Microsoft Store**, busca **"Ubuntu"** (el de Canonical) e instálalo.
7. Abre **Ubuntu** desde el menú Inicio. La primera vez te pedirá crear un usuario y contraseña de Linux.

Con eso ya tienes WSL (Ubuntu) sin usar `dism` ni `wsl` en PowerShell.

---

## Método 2: Si quieres probar con rutas completas (PowerShell Administrador)

A veces el problema es que PowerShell no encuentra los programas. Prueba con la ruta completa de `dism`:

1. Abre **PowerShell como administrador**.
2. Ejecuta **uno por uno**:

```powershell
C:\Windows\System32\dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

```powershell
C:\Windows\System32\dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

3. Reinicia el PC.
4. Luego instala **Ubuntu** desde **Microsoft Store** (paso 6 del Método 1).

Para instalar Ubuntu por comando (solo si ya funciona WSL):

```powershell
C:\Windows\System32\wsl.exe --install -d Ubuntu
```

---

## Después de tener Ubuntu instalado

1. Abre **Ubuntu** desde el menú Inicio.
2. Instala Buildozer (solo la primera vez):

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv build-essential openjdk-17-jdk unzip libffi-dev libssl-dev
pip install --user buildozer
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

3. Ve a tu proyecto y genera el APK:

```bash
cd /mnt/c/Users/Familia/AndroidStudioProjects/millonario_biblico
buildozer android debug
```

O desde Windows: ejecuta **generar_apk.bat** (el script ya usa la ruta completa de WSL).

---

## Resumen rápido

| Paso | Qué hacer |
|------|-----------|
| 1 | **Win + R** → escribir `optionalfeatures` → Aceptar |
| 2 | Marcar **Subsistema de Windows para Linux** y **Plataforma de máquina virtual** → Aceptar → Reiniciar |
| 3 | Abrir **Microsoft Store** → buscar **Ubuntu** → Instalar |
| 4 | Abrir **Ubuntu** del menú Inicio y crear usuario/contraseña |
| 5 | Dentro de Ubuntu, instalar Buildozer (comandos de arriba) y luego ejecutar `generar_apk.bat` o `buildozer android debug` |

Así no dependes de que PowerShell reconozca `dism` ni `wsl`.
