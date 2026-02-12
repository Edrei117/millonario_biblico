@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "WIN_PROJECT=%~dp0"
set "WIN_PROJECT=%WIN_PROJECT:~0,-1%"

echo.
echo ========================================
echo   Millonario Biblico - Generar APK
echo   (Kivy + Buildozer en WSL)
echo ========================================
echo.
echo Proyecto: %WIN_PROJECT%
echo.
echo Si no tienes WSL con Ubuntu, instala primero:
echo   wsl --install -d Ubuntu
echo.
echo La primera vez que generes el APK puede tardar 20-40 minutos.
echo.
echo Iniciando Buildozer en WSL...
echo.

set "WSL_CMD="
if exist "C:\Windows\System32\wsl.exe" set "WSL_CMD=C:\Windows\System32\wsl.exe"
if "%WSL_CMD%"=="" (
    where wsl.exe >nul 2>&1
    if not errorlevel 1 set "WSL_CMD=wsl.exe"
)
if "%WSL_CMD%"=="" (
    echo [ERROR] WSL no esta instalado.
    echo.
    echo Hazlo por MENUS, sin comandos: abre INSTALAR_WSL_WINDOWS.md
    echo Resumen: Win+R -^> escribe optionalfeatures -^> marca
    echo   "Subsistema de Windows para Linux" y "Plataforma de maquina virtual"
    echo Reinicia, luego instala "Ubuntu" desde Microsoft Store.
    echo.
    goto :fin
)

"%WSL_CMD%" -e bash -c "cd \"$(wslpath -u '%WIN_PROJECT%')\" && bash generar_apk_wsl.sh"

echo.
if exist "bin\*.apk" (
    echo ========================================
    echo   APK generado en la carpeta: bin\
    echo ========================================
    dir /b bin\*.apk 2>nul
    echo.
    echo Puedes copiar el .apk al escritorio o a tu telefono.
    explorer "bin"
) else (
    echo Revisa los mensajes de arriba por si hubo errores.
)
:fin
echo.
pause
