# 📁 Estructura del Proyecto - ¿Quién Quiere Ser Millonario? Bíblico

## 🎯 ¿Por qué esta estructura?

**Antes:** Todo estaba en `main.py` (747 líneas) - difícil de entender y mantener.

**Ahora:** Código organizado en módulos - fácil de entender, modificar y mantener.

---

## 📂 Estructura de Archivos

```
millonario_biblico/
│
├── main.py                 # ⭐ Punto de entrada - App principal
├── main.kv                 # Interfaz gráfica (diseño visual)
├── config.py               # ⚙️ Configuración y constantes
├── game_logic.py           # 🎮 Lógica del juego (preguntas, comodines)
│
├── screens/                # 📱 Pantallas del juego
│   ├── __init__.py
│   ├── splash_screen.py    # Pantalla de carga
│   ├── menu_screen.py      # Menú principal
│   └── game_screen.py       # Pantalla de juego
│
├── preguntas/              # 📚 Preguntas en JSON
│   └── preguntas_biblicas.json
│
├── sounds/                 # 🔊 Sonidos del juego
└── assets/                 # 🎨 Recursos gráficos
```

---

## 📄 Descripción de cada archivo

### 1. `main.py` (Aplicación Principal)
**¿Qué hace?**
- Es el punto de entrada de la aplicación
- Orquesta todas las pantallas
- Maneja la lógica del juego (preguntas, respuestas, comodines)
- Gestiona sonidos y recursos

**¿Cuándo modificarlo?**
- Para agregar nuevas funcionalidades al juego
- Para cambiar la lógica de preguntas/respuestas
- Para modificar comodines

---

### 2. `config.py` (Configuración)
**¿Qué contiene?**
- Lista de premios (`PREMIOS`)
- Niveles de seguridad (`SEGURIDAD`)
- Versículos bíblicos (`VERSICULOS_BIBLICOS`)

**¿Cuándo modificarlo?**
- Para cambiar los premios
- Para agregar más versículos
- Para modificar niveles de seguridad

**Ejemplo:**
```python
# Agregar un nuevo versículo
VERSICULOS_BIBLICOS.append(""Nuevo versículo..." (Libro X:Y)")
```

---

### 3. `screens/splash_screen.py` (Pantalla de Carga)
**¿Qué hace?**
- Muestra la pantalla de carga con barra de progreso
- Muestra versículos bíblicos aleatorios
- Cambia automáticamente al menú cuando termina

**¿Cuándo modificarlo?**
- Para cambiar la velocidad de carga
- Para modificar cómo se muestran los versículos
- Para cambiar el diseño de la pantalla de carga

---

### 4. `screens/menu_screen.py` (Menú Principal)
**¿Qué hace?**
- Muestra el menú principal con botones
- Maneja el inicio del juego
- Muestra las instrucciones

**¿Cuándo modificarlo?**
- Para agregar nuevos botones al menú
- Para cambiar las instrucciones
- Para modificar el diseño del menú

---

### 5. `screens/game_screen.py` (Pantalla de Juego)
**¿Qué hace?**
- Maneja la interacción del usuario durante el juego
- Procesa las selecciones de respuestas
- Maneja el uso de comodines

**¿Cuándo modificarlo?**
- Para cambiar cómo se manejan las respuestas
- Para modificar la interacción con comodines
- Para agregar nuevas funcionalidades a la pantalla de juego

---

### 6. `game_logic.py` (Lógica del Juego)
**¿Qué hace?**
- Maneja la carga de preguntas desde JSON
- Gestiona el estado del juego
- Calcula premios de seguridad

**Nota:** Este archivo está preparado para futuras mejoras. Por ahora, la lógica está en `main.py` para mantener la compatibilidad.

---

## 🎓 Ventajas de esta estructura

### ✅ **Más fácil de entender**
- Cada archivo tiene una responsabilidad clara
- Sabes dónde buscar cada cosa

### ✅ **Más fácil de modificar**
- ¿Quieres cambiar los versículos? → `config.py`
- ¿Quieres cambiar el menú? → `screens/menu_screen.py`
- ¿Quieres cambiar la lógica del juego? → `main.py`

### ✅ **Más fácil de mantener**
- Si algo se rompe, sabes dónde está el problema
- Puedes trabajar en una parte sin afectar otras

### ✅ **Más fácil de expandir**
- Agregar nuevas pantallas: crear archivo en `screens/`
- Agregar nuevas constantes: modificar `config.py`
- Agregar nuevas funcionalidades: modificar `main.py`

---

## 🔄 Flujo de la aplicación

```
1. main.py (inicia)
   ↓
2. SplashScreen (carga con versículos)
   ↓
3. MenuScreen (menú principal)
   ↓
4. GameScreen (juego)
   ↓
5. Vuelve a MenuScreen (al terminar)
```

---

## 💡 Consejos para trabajar con esta estructura

### **Para agregar un nuevo versículo:**
1. Abre `config.py`
2. Agrega el versículo a `VERSICULOS_BIBLICOS`
3. ¡Listo!

### **Para cambiar los premios:**
1. Abre `config.py`
2. Modifica la lista `PREMIOS`
3. ¡Listo!

### **Para agregar una nueva pantalla:**
1. Crea `screens/nueva_pantalla.py`
2. Importa en `screens/__init__.py`
3. Agrega en `main.py` → `build()`

### **Para modificar el diseño visual:**
1. Abre `main.kv`
2. Busca la sección correspondiente (ej: `<GameScreen>`)
3. Modifica el diseño

---

## 🚀 Próximos pasos sugeridos

1. **Separar más la lógica del juego** → Mover funciones de `main.py` a `game_logic.py`
2. **Crear un módulo de utilidades** → `utils.py` para funciones auxiliares
3. **Agregar tests** → Crear carpeta `tests/` para pruebas unitarias
4. **Documentar mejor** → Agregar más comentarios explicativos

---

## ❓ Preguntas frecuentes

**P: ¿Puedo volver a tener todo en un solo archivo?**
R: Sí, pero no es recomendable. Esta estructura es más profesional y mantenible.

**P: ¿Qué pasa si borro un archivo por error?**
R: El código dejará de funcionar. Usa control de versiones (Git) para evitar esto.

**P: ¿Puedo agregar más archivos?**
R: ¡Claro! Esta estructura es flexible. Agrega lo que necesites siguiendo la misma lógica.

---

## 📚 Recursos de aprendizaje

- **KivyMD Docs:** https://kivymd.readthedocs.io/
- **Python Modules:** https://docs.python.org/3/tutorial/modules.html
- **Code Organization:** https://realpython.com/python-application-layouts/

---

**¡Ahora tienes un código más organizado y fácil de entender! 🎉**


