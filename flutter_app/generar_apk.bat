@echo off
chcp 65001 >nul
echo Generando APK de Millonario Biblico (Flutter)...
echo.

cd /d "%~dp0"

where flutter >nul 2>&1
if errorlevel 1 (
    echo ERROR: Flutter no esta en el PATH.
    echo Instala Flutter y anade la carpeta bin al PATH.
    echo Ver COMO_GENERAR_APK.md para instrucciones.
    pause
    exit /b 1
)

echo Ejecutando: flutter pub get
flutter pub get
if errorlevel 1 (
    echo Fallo flutter pub get
    pause
    exit /b 1
)

echo.
echo Ejecutando: flutter build apk
flutter build apk
if errorlevel 1 (
    echo Fallo la compilacion.
    pause
    exit /b 1
)

echo.
echo ========================================
echo APK generado correctamente.
echo Ubicacion:
echo   build\app\outputs\flutter-apk\app-release.apk
echo ========================================
explorer "build\app\outputs\flutter-apk"
pause
