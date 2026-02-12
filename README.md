# ¿Quién Quiere Ser Millonario? Bíblico

Una aplicación móvil tipo "¿Quién quiere ser millonario?" con preguntas bíblicas, desarrollada con Kivy/KivyMD.

## Características

- ✅ 15 niveles de preguntas bíblicas
- ✅ Sistema de premios progresivo ($100 hasta $1,000,000)
- ✅ 3 comodines disponibles:
  - **50/50**: Elimina 2 respuestas incorrectas
  - **Llamada**: Te ayuda con una pista
  - **Público**: Muestra resultados de votación simulada
- ✅ Niveles de seguridad en las preguntas 5 y 10
- ✅ Interfaz moderna y responsiva para dispositivos móviles

## Instalación

### Requisitos
- Python 3.8 o superior
- Kivy 2.3.1
- KivyMD 1.2.0

### Instalación de dependencias

```bash
pip install kivy==2.3.1 kivymd==1.2.0 pillow
```

## Ejecución

### En Windows
```bash
python main.py
```
Usa **main.py** (carga en el hilo principal, todo con audio).

### En Linux / Ubuntu (incl. VirtualBox)
```bash
python main_linux.py
```
O bien: `./run_app.sh` (ejecuta main_linux.py). En Linux se usa **main_linux.py**, que carga preguntas y sonidos en hilos para no bloquear la ventana. Ver **EJECUTAR_APP_UBUNTU.md**.

### Para Android (APK)

**Recomendado (sin Linux en tu PC):** Sube el proyecto a GitHub y usa GitHub Actions. Ver **COMO_GENERAR_APK_SIN_LINUX.md**.

**Con Linux/WSL:** Instala Buildozer y ejecuta `buildozer android debug`. Ver **COMO_GENERAR_APK_KIVY.md**.

## Estructura del Proyecto

```
millonario_biblico/
├── main.py              # Código principal de la aplicación
├── main.kv              # Diseño de la interfaz (Kivy)
├── buildozer.spec       # Configuración para compilar APK
├── preguntas/           # Preguntas bíblicas en formato JSON
│   └── preguntas_biblicas.json
├── sounds/              # Sonidos opcionales (click, correct, wrong)
└── assets/              # Imágenes y recursos opcionales
```

## Agregar Más Preguntas

Puedes agregar más preguntas editando el archivo `preguntas/preguntas_biblicas.json`:

```json
{
  "dificultad": "variable",
  "preguntas": [
    {
      "pregunta": "Tu pregunta aquí",
      "opciones": ["Opción A", "Opción B", "Opción C", "Opción D"],
      "respuesta_correcta": 0,
      "nivel": 1
    }
  ]
}
```

Nota: `respuesta_correcta` es el índice (0-3) de la opción correcta.

## Reglas del Juego

1. Responde 15 preguntas bíblicas para ganar $1,000,000
2. Cada pregunta tiene 4 opciones (A, B, C, D)
3. Puedes usar 3 comodines por partida (uno de cada tipo)
4. Los niveles de seguridad garantizan un premio mínimo:
   - Pregunta 5: $1,000 garantizado
   - Pregunta 10: $32,000 garantizado
5. Si respondes incorrectamente, pierdes y te retiras con el premio del último nivel de seguridad alcanzado

## Personalización

- **Colores**: Edita los colores en `main.kv` para cambiar el tema visual
- **Sonidos**: Agrega archivos `.wav` en la carpeta `sounds/`
- **Preguntas**: Edita los archivos JSON en `preguntas/`

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

