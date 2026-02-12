# ¿Quién Quiere Ser Millonario? Bíblico (Flutter)

Versión en **Flutter** del juego. Puedes abrirla en **Android Studio** y ejecutarla en emuladores o dispositivos sin usar Buildozer ni WSL.

## Requisitos

- [Flutter SDK](https://docs.flutter.dev/get-started/install) instalado y en el PATH.
- Android Studio (opcional pero recomendado para emuladores).

## Usar el banco de preguntas completo

El proyecto incluye un JSON mínimo. Para usar todas tus preguntas:

1. Copia el archivo del proyecto Kivy a esta carpeta:
   - **Origen:** `../preguntas/preguntas_biblicas.json`
   - **Destino:** `assets/preguntas/preguntas_biblicas.json`
2. Sobrescribe el archivo actual.

En PowerShell (desde la raíz del repo):

```powershell
Copy-Item "preguntas\preguntas_biblicas.json" -Destination "flutter_app\assets\preguntas\"
```

## Abrir en Android Studio

1. Abre Android Studio.
2. **File → Open** y selecciona la carpeta **`flutter_app`** (esta carpeta).
3. Espera a que termine de indexar y que aparezca "Pub get" si lo pide.
4. En la barra superior elige un dispositivo (emulador o físico) y pulsa **Run (▶)**.

## Probar en varios dispositivos virtuales

1. **Tools → Device Manager** en Android Studio.
2. Crea varios AVD (por ejemplo: Pixel 6, pantalla pequeña, tablet).
3. Elige cada uno en el selector y ejecuta la app para ver cómo se ve en cada uno.

## Comandos por terminal

Desde esta carpeta (`flutter_app`):

```bash
# Obtener dependencias
flutter pub get

# Ejecutar en un dispositivo/emulador conectado
flutter run

# Ejecutar en un emulador concreto (lista con: flutter devices)
flutter run -d <device_id>

# Generar APK (Android 7+ / minSdk 24)
flutter build apk
```

El APK se genera en `build/app/outputs/flutter-apk/app-release.apk`.

## Estructura

- `lib/main.dart` – App y rutas.
- `lib/config.dart` – Premios, seguridad, versículos.
- `lib/models/question.dart` – Modelo de pregunta.
- `lib/services/game_service.dart` – Lógica del juego (Provider).
- `lib/screens/` – Splash, menú, juego.
- `lib/widgets/prize_ladder.dart` – Escalera de premios.
- `assets/preguntas/` – JSON de preguntas.

## Compatibilidad

- **Android:** minSdk 24 (Android 7.0 en adelante).
- Interfaz responsive para distintos tamaños de pantalla.
