# Guía completa del código – Millonario Bíblico

Esta guía explica **cada parte del proyecto**: librerías, imports, archivos y flujo, para que puedas entenderlo y hacer algo parecido por tu cuenta.

---

## 1. Librerías e importaciones

### 1.1 Librerías de Python (estándar)

```python
import os
```
- **Qué es:** Módulo estándar de Python para trabajar con el sistema operativo.
- **Para qué se usa aquí:**
  - `os.path.dirname()`, `os.path.abspath()` → Obtener la ruta de la carpeta del proyecto.
  - `os.path.join()` → Unir carpetas (ej: `preguntas/archivo.json`).
  - `os.listdir()` → Listar archivos en una carpeta.
  - `os.path.exists()`, `os.makedirs()` → Comprobar si existe una carpeta y crearla.
- **En tu proyecto:** Cualquier app que lea archivos o carpetas (config, datos, sonidos) usará `os`.

---

### 1.2 Kivy (base gráfica)

**Kivy** es un framework para crear interfaces gráficas (ventanas, botones, pantallas) en Python. No es KivyMD todavía; Kivy es la base.

```python
from kivy.lang import Builder
```
- **Qué hace:** Carga y aplica archivos **.kv** (diseño en un lenguaje parecido a YAML).
- **Uso en el proyecto:** `Builder.load_file("main.kv")` carga todo el diseño de pantallas y botones.
- **En tu proyecto:** Si usas archivos `.kv` para la interfaz, siempre harás `from kivy.lang import Builder` y `Builder.load_file("tu_archivo.kv")`.

```python
from kivy.core.window import Window
```
- **Qué hace:** Controla la ventana de la aplicación (tamaño, título, etc.).
- **Uso en el proyecto:** `Window.minimum_width = 320` y `Window.minimum_height = 480` para definir tamaño mínimo.
- **En tu proyecto:** Para fijar tamaño de ventana, pantalla completa o propiedades de la ventana.

```python
from kivy.uix.screenmanager import ScreenManager, FadeTransition, SlideTransition
```
- **Qué hace:**
  - **ScreenManager:** Contenedor que muestra una pantalla a la vez (como un “cubo” de pantallas) y permite cambiar entre ellas.
  - **FadeTransition / SlideTransition:** Animaciones al cambiar de pantalla (fundido o deslizamiento).
- **Uso en el proyecto:** Se crea un `ScreenManager`, se le añaden las pantallas y se cambia con `self.sm.current = 'menu'` o `'juego'`.
- **En tu proyecto:** Cualquier app con varias “pantallas” (menú, juego, configuración) usará `ScreenManager` y transiciones.

```python
from kivy.core.audio import SoundLoader
```
- **Qué hace:** Carga y reproduce archivos de audio (WAV, OGG, etc.).
- **Uso en el proyecto:** `SoundLoader.load('sounds/correct.wav')` y luego `sound.play()`.
- **En tu proyecto:** Sonidos de clic, acierto, error, música de fondo.

```python
from kivy.clock import Clock
```
- **Qué hace:** Programar acciones para más tarde (en segundos o de forma repetida).
- **Uso en el proyecto:**
  - `Clock.schedule_once(función, segundos)` → Ejecutar una vez después de X segundos.
  - `Clock.schedule_interval(función, segundos)` → Ejecutar cada X segundos (timer, barra de carga).
- **En tu proyecto:** Timers, retrasos (por ejemplo “esperar 2 segundos y luego siguiente pregunta”), animaciones por tiempo.

---

### 1.3 KivyMD (Material Design sobre Kivy)

**KivyMD** es una librería que añade componentes con estilo **Material Design** (botones, tarjetas, diálogos, barras de progreso) sobre Kivy.

```python
from kivymd.app import MDApp
```
- **Qué hace:** Clase base de la aplicación. Tu app hereda de `MDApp` (igual que en Kivy se hereda de `App`).
- **Uso en el proyecto:** `class MillonarioApp(MDApp):` y al final `MillonarioApp().run()`.
- **En tu proyecto:** El “corazón” de la app: una sola clase que hereda de `MDApp` y tiene al menos el método `build()`.

```python
from kivymd.uix.screen import MDScreen
```
- **Qué hace:** Una pantalla completa (una “página” dentro del `ScreenManager`). Cada pantalla es un `MDScreen`.
- **Uso en el proyecto:** `SplashScreen`, `MenuScreen` y `GameScreen` heredan de `MDScreen`.
- **En tu proyecto:** Una clase por cada pantalla (menú, juego, opciones, etc.).

```python
from kivymd.uix.button import MDRaisedButton, MDFlatButton
```
- **Qué hace:**
  - **MDRaisedButton:** Botón con relieve/relleno (resalta más).
  - **MDFlatButton:** Botón plano (solo texto o borde).
- **Uso en el proyecto:** Botones “Iniciar juego”, “Instrucciones”, opciones A/B/C/D, “Cerrar” en diálogos.
- **En tu proyecto:** Cualquier botón en la interfaz.

```python
from kivymd.uix.label import MDLabel
```
- **Qué hace:** Texto en pantalla (títulos, subtítulos, preguntas, porcentajes).
- **Uso en el proyecto:** Títulos, pregunta actual, opciones, “0%”, “Cargando...”, versículos.
- **En tu proyecto:** Todo lo que sea solo texto.

```python
from kivymd.uix.boxlayout import MDBoxLayout
```
- **Qué hace:** Contenedor que ordena los widgets en fila (horizontal) o columna (vertical).
- **Uso en el proyecto:** Organizar botones, etiquetas y barras en vertical u horizontal.
- **En tu proyecto:** Casi todas las pantallas usan `MDBoxLayout` para ordenar elementos.

```python
from kivymd.uix.card import MDCard
```
- **Qué hace:** “Tarjeta” con fondo y bordes redondeados (estilo Material).
- **Uso en el proyecto:** Cada opción A/B/C/D es una tarjeta; la escalera de premios son tarjetas por nivel.
- **En tu proyecto:** Bloques visuales (opciones, niveles, items de lista).

```python
from kivymd.uix.dialog import MDDialog
```
- **Qué hace:** Ventana emergente (diálogo) con título, texto y botones.
- **Uso en el proyecto:** Instrucciones, “Llamada a un amigo”, “Consulta al público”, “Fin del juego”.
- **En tu proyecto:** Cualquier popup (mensajes, confirmaciones, instrucciones).

---

### 1.4 Imports del propio proyecto

```python
from config import PREMIOS, SEGURIDAD
```
- **Qué hace:** Trae constantes del archivo `config.py` (lista de premios y niveles de seguridad).
- **Para qué:** Centralizar configuración para no tener números y textos repartidos por todo el código.

```python
from screens import SplashScreen, MenuScreen, GameScreen
```
- **Qué hace:** Trae las clases de las tres pantallas definidas en la carpeta `screens/`.
- **Para qué:** Poder hacer `SplashScreen(name='splash')`, `MenuScreen()`, `GameScreen()` en `build()`.

```python
from kivy.resources import resource_add_path
```
- **Qué hace:** Añade carpetas donde Kivy busca recursos (imágenes, sonidos, fuentes).
- **Uso en el proyecto:** Se añaden `BASE_DIR`, `assets`, `sounds`, `preguntas` para que las rutas relativas funcionen bien al ejecutar desde otra carpeta.

---

## 2. Archivo `config.py`

**Función:** Guardar constantes que usa el resto del proyecto.

| Constante | Tipo | Uso |
|-----------|------|-----|
| `PREMIOS` | Lista de strings | Premio en dinero por cada nivel (1 a 15). |
| `SEGURIDAD` | Lista [5, 10] | Niveles en los que se “asegura” el premio al fallar. |
| `VERSICULOS_BIBLICOS` | Lista de strings | Textos que se muestran en la pantalla de carga. |

Así puedes cambiar premios o versículos en un solo sitio sin tocar la lógica del juego.

---

## 3. Archivo `main.py` – Aplicación principal

### 3.1 Configuración de rutas (principio del archivo)

```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
resource_add_path(BASE_DIR)
...
```
- **Qué hace:**  
  - `BASE_DIR` = carpeta donde está `main.py`.  
  - `os.chdir(BASE_DIR)` = la “carpeta de trabajo” es la del proyecto.  
  - `resource_add_path(...)` = Kivy busca archivos (sonidos, etc.) también en esas carpetas.
- **Para qué:** Que `sounds/correct.wav`, `preguntas/preguntas_biblicas.json`, etc. se encuentren aunque ejecutes desde otro directorio.

### 3.2 Clase `MillonarioApp(MDApp)`

Es la aplicación: una sola instancia que vive durante toda la ejecución.

**`__init__`:**
- Inicializa el estado del juego: `preguntas`, `pregunta_actual`, `pregunta_indice`, `comodines_usados`, `premio_actual`, `sounds`, `game_in_progress`, `sm` (ScreenManager), `timer_event`, `tiempo_restante`.
- Todo lo que debe “recordar” la app entre pantallas y preguntas va aquí.

**`build()`:**
1. Define el título de la ventana.
2. Configura tamaño mínimo con `Window`.
3. Crea el `ScreenManager` (`self.sm`).
4. Carga el diseño con `Builder.load_file("main.kv")`.
5. Añade las tres pantallas: `SplashScreen`, `MenuScreen`, `GameScreen`.
6. Carga sonidos y preguntas.
7. Pone la pantalla actual en `'splash'`.
8. Devuelve `self.sm` (que es la raíz de la interfaz).

**`cargar_sonidos()`:**  
Crea la carpeta `sounds` si no existe, carga `click.wav`, `correct.wav`, `wrong.wav` con `SoundLoader` y les pone volumen 0.5. Si no existen los archivos, no rompe; solo no habrá sonido.

**`cargar_preguntas()`:**  
1. Busca archivos `.json` en la carpeta `preguntas`.  
2. En cada JSON lee la lista `preguntas` y la une a `all_questions`.  
3. Mezcla con `random.shuffle` y toma 15 preguntas.  
4. Si no hay suficientes, rellena repitiendo y luego corta a 15.  
5. Si no hay carpeta o hay error, usa `crear_preguntas_ejemplo()`.

**`crear_preguntas_ejemplo()`:**  
Crea la carpeta `preguntas` y, si no existe, un `preguntas_biblicas.json` mínimo con una pregunta de ejemplo. Así la app puede arrancar aunque no tengas aún tus JSON.

**`resetear_juego()`:**  
- Cancela el timer si estaba activo.  
- Pone `pregunta_indice = 0`, comodines no usados, premios a 0, `tiempo_restante = 30`, `game_in_progress = True`.  
- Vuelve a mezclar `self.preguntas`.  
Se llama al pulsar “Iniciar juego”.

**`cargar_pregunta_actual()`:**  
1. Si no hay juego en curso o ya no quedan preguntas, llama a `finalizar_juego()`.  
2. Cancela el timer anterior y pone `tiempo_restante = 30`.  
3. Toma `self.pregunta_actual = self.preguntas[self.pregunta_indice]`.  
4. Obtiene la pantalla de juego con `self.sm.get_screen('juego')`.  
5. Actualiza en esa pantalla: texto de la pregunta, texto de las 4 opciones, colores y estado de las “cards”, número de nivel, texto del timer.  
6. Llama a `actualizar_lista_premios()` y `actualizar_comodines()`.  
7. Inicia el timer con `iniciar_timer()`.

**`actualizar_lista_premios()`:**  
- Limpia el contenedor `premios_list` en la pantalla de juego.  
- Para niveles 1–10 crea una tarjeta por nivel con número, premio y etiquetas “Seguro 1/2” donde toque.  
- Pinta de distinto color el nivel actual, los ya superados y los que faltan.

**`actualizar_comodines()`:**  
- Según `self.comodines_usados`, deshabilita y baja la opacidad de los botones 50/50 y público cuando ya se usaron.

**`iniciar_timer()` / `actualizar_timer()`:**  
- `iniciar_timer()` programa con `Clock.schedule_interval` que cada segundo se llame a `actualizar_timer()`.  
- `actualizar_timer()` resta 1 a `tiempo_restante`, actualiza el texto del timer en pantalla (y color si ≤ 10 s). Si llega a 0, cancela el timer y llama a `procesar_respuesta_tiempo_agotado()`.

**`procesar_respuesta_tiempo_agotado()`:**  
- Deshabilita todas las opciones, marca la respuesta correcta en verde, opcionalmente reproduce sonido de error, pone el timer a 0 y a los 2 segundos llama a `finalizar_juego(ganador=False)`.

**`procesar_respuesta(indice)`:**  
1. Cancela el timer.  
2. Deshabilita todas las opciones.  
3. Compara `indice` con `respuesta_correcta` de la pregunta actual.  
4. Pinta la opción correcta en verde y, si falló, la elegida en rojo.  
5. Reproduce sonido correcto o incorrecto.  
6. Si acertó: a los 2 segundos incrementa `pregunta_indice`, actualiza premio y seguridad, y llama a `cargar_pregunta_actual()`.  
7. Si falló: a los 2 segundos llama a `finalizar_juego(ganador=False)`.

**`usar_comodin(tipo)`:**  
- Si el comodín ya estaba usado, no hace nada.  
- Marca el comodín como usado y llama a `comodin_50_50()`, `comodin_llamada()` o `comodin_publico()`.  
- Luego actualiza la vista de comodines.

**`comodin_50_50()`:**  
- Elige 2 opciones incorrectas (excluyendo la correcta) con `random.sample`.  
- Esas dos opciones las deshabilita y les baja opacidad en la pantalla.

**`comodin_llamada()`:**  
- Muestra un `MDDialog` con un texto de “pista” que sugiere la opción correcta (elegida al azar entre varias frases).

**`comodin_publico()`:**  
- Genera porcentajes para A, B, C, D (la correcta con más %).  
- Muestra un `MDDialog` con “Resultados de la votación del público”.

**`finalizar_juego(ganador)`:**  
- Cancela el timer y pone `game_in_progress = False`.  
- Calcula el premio final según si ganó o en qué nivel de seguridad quedó.  
- Abre un `MDDialog` con el mensaje y premio, y botones “Nuevo Juego” y “Salir”.

**`nuevo_juego(dialog)` / `salir_juego(dialog)`:**  
- Cierran el diálogo y llaman a `cambiar_pantalla('menu', 'right')`.

**`cambiar_pantalla(nombre_pantalla, direccion)`:**  
- Asigna la transición (Slide o Fade) según `direccion` y hace `self.sm.current = nombre_pantalla`.

---

## 4. Pantallas (`screens/`)

### 4.1 `splash_screen.py`

- **Imports:** `MDScreen`, `Clock`, `random`, `VERSICULOS_BIBLICOS` de `config`.
- **SplashScreen** guarda `progress`, `progress_event` y la lista de versículos.
- **`on_enter()`:** Al mostrarse la pantalla, reinicia progreso, actualiza versículo y barra, y programa con `Clock.schedule_interval` que cada 0.08 s se llame a `_actualizar_carga`.
- **`_actualizar_carga(dt)`:** Suma 2 al progreso. Si llega a 100, cancela el intervalo, actualiza la barra y llama a `ir_a_menu()`. Cada 25% puede cambiar el versículo mostrado.
- **`ir_a_menu()`:** Obtiene la app con `MDApp.get_running_app()` y pone `app.sm.current = "menu"`.

Así la pantalla de carga “corre sola” y al terminar pasa al menú.

### 4.2 `menu_screen.py`

- **Imports:** `MDScreen`, `MDRaisedButton`, `MDDialog`.
- **`iniciar_juego()`:** Obtiene la app, llama a `app.resetear_juego()` y `app.cambiar_pantalla('juego', 'left')`.
- **`mostrar_instrucciones()`:** Crea un `MDDialog` con título “Instrucciones” y un texto largo con las reglas; un botón “Cerrar” que hace `dialog.dismiss()`.

La pantalla solo delega en la app; no contiene lógica de juego.

### 4.3 `game_screen.py`

- **Imports:** `MDScreen`, `MDRaisedButton`, `MDDialog`, `Clock`.
- **`on_enter()`:** Al entrar en la pantalla de juego, obtiene la app y llama a `app.cargar_pregunta_actual()`.
- **`seleccionar_respuesta(indice)`:** Guarda el índice y llama a `app.procesar_respuesta(indice)`.
- **`usar_comodin(tipo)`:** Llama a `app.usar_comodin(tipo)`.
- **`mostrar_feedback(mensaje, correcto)`:** Abre un diálogo y lo cierra a los 1.5 s con `Clock.schedule_once`.

La pantalla de juego solo reenvía las acciones del usuario a la app; la lógica está en `main.py`.

---

## 5. Archivo `main.kv` – Interfaz gráfica

**Kv** es el lenguaje de Kivy para describir la interfaz (widgets, disposición, propiedades) sin escribir todo en Python.

### 5.1 Cabecera e imports

```text
#:kivy 2.0.0
#:import FadeTransition ...
#:import SlideTransition ...
```
- La primera línea indica versión de Kivy para el archivo.
- `#:import` permite usar clases de Python en el KV (por ejemplo para transiciones o layouts).

### 5.2 Reglas por clase

Cada bloque `<NombreClase>:` define cómo se ve y se estructura esa clase (que en Python hereda de `MDScreen` o similar).

**Dentro de una regla:**
- **`canvas.before:`** – Dibujo detrás del widget (fondos, bordes). Aquí se usa `Color` y `Rectangle` para el fondo.
- **`MDBoxLayout:`** – Contenedor vertical u horizontal.
- **`MDLabel:`** – Texto. Propiedades típicas: `text`, `halign`, `font_style`, `theme_text_color`, `text_color`, `size_hint_y`, `height`.
- **`id: nombre`** – Asigna un id para acceder desde Python con `self.ids.nombre` (por ejemplo `progress_bar`, `pregunta_text`, `opcion_a`).
- **`on_release: root.metodo(args)`** – Al soltar el botón se llama a `metodo` en la pantalla (`root` = pantalla actual).

**Unidades:**  
- `dp` = densidad independiente (tamaños que escalan con la pantalla).  
- `sp` = para fuentes.

**Colores:**  
- `rgba: R, G, B, A` con valores 0–1 (ej: `1, 0.84, 0, 1` = dorado).

Con esto puedes leer cualquier sección de `main.kv` y saber: qué pantalla es, qué botones hay, qué ids usan y qué método de `root` se ejecuta al pulsar.

---

## 6. Datos: `preguntas_biblicas.json`

Estructura típica:

```json
{
  "dificultad": "variable",
  "preguntas": [
    {
      "pregunta": "¿Texto de la pregunta?",
      "opciones": ["A", "B", "C", "D"],
      "respuesta_correcta": 1,
      "nivel": 1
    }
  ]
}
```

- **`respuesta_correcta`:** Índice en `opciones` (0 = A, 1 = B, 2 = C, 3 = D).
- El código usa `data.get('preguntas', [])` y luego mezcla y toma 15 preguntas.

Para hacer un juego parecido con otro tema, basta con otro JSON con la misma estructura (o la que definas y adaptes en `cargar_preguntas()`).

---

## 7. Flujo general de la aplicación

1. Se ejecuta `MillonarioApp().run()`.
2. Se llama a `build()`: se crea el `ScreenManager`, se carga `main.kv`, se añaden las 3 pantallas, se cargan sonidos y preguntas, y la pantalla actual es `splash`.
3. **Splash:** Al entrar, se inicia el intervalo que sube la barra y cambia versículos; al llegar a 100% se hace `app.sm.current = 'menu'`.
4. **Menú:** El usuario puede “Iniciar juego” (resetear y ir a `juego`) o “Instrucciones” (abrir diálogo).
5. **Juego:** Al entrar se llama a `cargar_pregunta_actual()`: se muestra la pregunta, opciones, timer y escalera de premios. El usuario responde o usa comodines; cada acción se procesa en `main.py` (procesar_respuesta, usar_comodin, etc.). Si acierta se carga la siguiente pregunta; si falla o se acaba el tiempo se llama a `finalizar_juego()`.
6. Al finalizar se muestra el diálogo de resultado; “Nuevo Juego” o “Salir” vuelven al menú.

---

## 8. Cómo hacer un proyecto similar por tu cuenta

1. **Estructura mínima:**  
   - Un `main.py` con una clase que herede de `MDApp`, método `build()` que devuelva un `ScreenManager`.  
   - Un `main.kv` con al menos una pantalla (`MDScreen`).

2. **Varias pantallas:**  
   - Crear una clase por pantalla (heredando de `MDScreen`).  
   - En `build()`, añadir cada pantalla al `ScreenManager`.  
   - En el KV, definir una regla `<NombreClase>:` para cada una.  
   - Cambiar de pantalla con `self.sm.current = 'nombre_pantalla'`.

3. **Datos externos:**  
   - Usar `json.load()` / `json.dump()` para cargar y guardar (preguntas, configuración).  
   - Usar `os` para rutas y existencia de carpetas/archivos.

4. **Timers y retrasos:**  
   - `Clock.schedule_once` para “dentro de X segundos”.  
   - `Clock.schedule_interval` para “cada X segundos” (y cancelar cuando no lo necesites).

5. **Comunicación pantalla ↔ app:**  
   - La app tiene `self.sm` y estado (preguntas, índice, etc.).  
   - Las pantallas obtienen la app con `MDApp.get_running_app()` y llaman a métodos de la app (`cargar_pregunta_actual`, `procesar_respuesta`, etc.).  
   - La app actualiza la UI accediendo a `self.sm.get_screen('juego').ids.nombre_widget`.

6. **Ids en KV:**  
   - Pon `id: algo` en los widgets que necesites cambiar desde Python (textos, barras, botones).  
   - Así puedes hacer `pantalla.ids.algo.text = "..."` o `pantalla.ids.algo.value = 50`.

Con esta guía tienes explicado cada librería, cada import, cada archivo y el flujo completo; puedes usar el mismo esquema para otro juego o app con preguntas, varias pantallas y datos en JSON.
