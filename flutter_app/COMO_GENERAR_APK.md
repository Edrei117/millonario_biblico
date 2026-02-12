# Cómo generar el APK

Tienes **dos versiones** del juego. Solo la de **Flutter** puede generar APK desde Windows sin WSL.

---

## Opción 1: APK con Flutter (recomendado, desde Windows)

### 1. Instalar Flutter (si aún no lo tienes)

1. Descarga Flutter SDK: https://docs.flutter.dev/get-started/install/windows  
2. Descomprime en una carpeta, por ejemplo: `C:\flutter`  
3. Añade Flutter al PATH:
   - Busca "variables de entorno" en Windows.
   - En "Variables del sistema" edita **Path**.
   - Añade la ruta a la carpeta **bin** de Flutter, por ejemplo: `C:\flutter\bin`
4. Cierra y vuelve a abrir la terminal (o Android Studio).

### 2. Comprobar que Flutter funciona

Abre **PowerShell** o la **terminal de Android Studio** y ejecuta:

```powershell
flutter doctor
```

Si todo está bien, verás marcas verdes. Si falta algo (Android SDK, etc.), sigue lo que indique.

### 3. Generar el APK

En PowerShell o en la terminal de Android Studio:

```powershell
cd "C:\Users\Familia\AndroidStudioProjects\millonario_biblico\flutter_app"
flutter pub get
flutter build apk
```

La primera vez puede tardar varios minutos (descarga dependencias y compila).

### 4. Dónde está el APK

Cuando termine sin errores, el archivo estará en:

```
flutter_app\build\app\outputs\flutter-apk\app-release.apk
```

Puedes copiar ese `.apk` al móvil (por USB, correo, Drive, etc.) e instalarlo. En el móvil puede que tengas que permitir "Instalar desde fuentes desconocidas" para ese archivo o para Chrome/Files.

---

## Opción 2: APK con la versión Kivy (Python)

La versión Kivy (main.py, buildozer) **no** puede generar el APK desde Windows. Buildozer solo funciona en **Linux**.

Opciones:

- **A)** Usar **WSL (Ubuntu)** en Windows, instalar buildozer ahí y ejecutar `buildozer android debug` dentro del proyecto (carpeta `millonario_biblico`, no `flutter_app`).
- **B)** Usar la **versión Flutter** (Opción 1) para generar el APK en Windows; es la forma más sencilla.

---

## Resumen rápido (Flutter)

1. Instalar Flutter y añadirlo al PATH.  
2. `cd` a la carpeta `flutter_app`.  
3. `flutter pub get` y luego `flutter build apk`.  
4. APK en: `flutter_app\build\app\outputs\flutter-apk\app-release.apk`.

Si al ejecutar `flutter build apk` sale algún error, copia el mensaje completo y lo revisamos.
