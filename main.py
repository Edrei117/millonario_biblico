"""
Aplicación principal: ¿Quién Quiere Ser Millonario? Bíblico

Punto de entrada para Windows. Orquesta pantallas y lógica del juego.
En Linux usa main_linux.py para evitar bloqueos en VM/carpetas compartidas.
"""
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition, SlideTransition
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image as KivyImage
import os

# Importar configuración
from config import PREMIOS, SEGURIDAD

# Importar pantallas
from screens import SplashScreen, MenuScreen, GameScreen

# Configurar rutas de recursos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    from kivy.resources import resource_add_path
    os.chdir(BASE_DIR)
    resource_add_path(BASE_DIR)
    resource_add_path(os.path.join(BASE_DIR, 'assets'))
    resource_add_path(os.path.join(BASE_DIR, 'sounds'))
    resource_add_path(os.path.join(BASE_DIR, 'audio'))
    resource_add_path(os.path.join(BASE_DIR, 'preguntas'))
    resource_add_path(os.path.join(BASE_DIR, 'comodines'))
    resource_add_path(os.path.join(BASE_DIR, 'assets', 'comodines'))
except Exception:
    pass

# Carpetas donde buscar imágenes de comodines (solo dentro del proyecto para APK)
COMODINES_DIRS = [
    os.path.join(BASE_DIR, 'assets', 'comodines'),
    os.path.join(BASE_DIR, 'comodines'),
]
# Carpetas donde buscar audio para cada pregunta (dentro del proyecto para que funcione en APK)
AUDIOS_DIRS = [
    os.path.join(BASE_DIR, 'sounds'),   # mismo lugar que click, correct, wrong
    os.path.join(BASE_DIR, 'audios'),
    os.path.join(BASE_DIR, 'audio'),
]
# id del botón en KV, nombre del archivo
IMAGENES_COMODINES = [
    ("comodin_50_50", "ayudasrecurso-1.png"),
    ("comodin_publico", "ayudasrecurso-1 (1).png"),
    ("comodin_busqueda_biblica", "llamada.jpg"),
]


class ImageButton(ButtonBehavior, KivyImage):
    """Botón que muestra una imagen y recibe clics correctamente."""
    pass


class MillonarioApp(MDApp):
    """
    Aplicación principal del juego.

    Responsabilidades:
    - Gestionar el ciclo de vida de la app
    - Coordinar las pantallas
    - Manejar la lógica del juego (preguntas, respuestas, comodines)
    - Gestionar sonidos y recursos
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Estado del juego
        self.preguntas = []
        self.pregunta_actual = None
        self.pregunta_indice = 0
        self.comodines_usados = {
            '50/50': False,
            'llamada': False,
            'publico': False,
            'busqueda_biblica': False
        }
        self.premio_actual = 0
        self.premio_seguridad = 0
        self.sounds = {}
        self.game_in_progress = False
        self.sm = None
        self.timer_event = None
        self.tiempo_restante = 30
        self._indice_ultima_pregunta_con_audio = -1  # para sonar solo una vez por pregunta
        self._cargando_pregunta_actual = False  # cerrojo para no entrar dos veces
        self._schedule_primera_pregunta = None  # para cancelar si se inicia de nuevo
        self._sonido_pregunta_playing = False  # True mientras suena el audio de pregunta
        self._sonido_pregunta_stop_event = None  # evento programado para detener el sonido

    def build(self):
        """Construye la interfaz de la aplicación."""
        self.title = "¿Quién Quiere Ser Millonario? Bíblico"
        try:
            Window.minimum_width = 320
            Window.minimum_height = 480
        except Exception:
            pass

        # Crear ScreenManager
        self.sm = ScreenManager()
        
        # Cargar archivo KV (interfaz gráfica) con ruta absoluta
        Builder.load_file(os.path.join(BASE_DIR, "main.kv"))
        
        # Agregar pantallas
        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(MenuScreen())
        self.sm.add_widget(GameScreen())
        
        # Cargar recursos después del primer frame (evita ventana en blanco / "not responding" en VM)
        Clock.schedule_once(self._cargar_recursos, 0)
        
        # Empezar en la pantalla de carga
        self.sm.current = 'splash'
        return self.sm

    def _cargar_recursos(self, dt):
        """Carga preguntas y sonidos en el hilo principal (Windows)."""
        try:
            self.cargar_preguntas()
        except Exception as e:
            print(f"[Millonario] Error cargando preguntas: {e}")
        Clock.schedule_once(self._cargar_sonidos_diferido, 2.0)

    def _cargar_sonidos_diferido(self, dt):
        """Carga sonidos 2 s después del inicio para no bloquear la ventana."""
        try:
            self.cargar_sonidos()
        except Exception as e:
            print(f"[Millonario] Error cargando sonidos (la app sigue sin audio): {e}")

    def cargar_sonidos(self):
        """Carga los archivos de sonido del juego."""
        sounds_dir = os.path.join(BASE_DIR, 'sounds')
        if not os.path.exists(sounds_dir):
            try:
                os.makedirs(sounds_dir, exist_ok=True)
            except Exception:
                pass
        
        # Intentar cargar sonidos (opcional - no crítico si no existen)
        self.sounds['click'] = SoundLoader.load(os.path.join(sounds_dir, 'click.wav'))
        self.sounds['correct'] = SoundLoader.load(os.path.join(sounds_dir, 'correct.wav'))
        self.sounds['wrong'] = SoundLoader.load(os.path.join(sounds_dir, 'wrong.wav'))
        
        # Sonido al empezar cada pregunta: buscar en sounds, audios, audio (solo rutas del proyecto)
        self.sounds['pregunta'] = None
        nombres_preferidos = ['audio editado_pregunta.mp3', 'pregunta.wav', 'pregunta.ogg', 'question.wav', 'question.ogg']
        for audio_dir in AUDIOS_DIRS:
            if not os.path.isdir(audio_dir):
                continue
            for nombre in nombres_preferidos:
                ruta = os.path.join(audio_dir, nombre)
                if os.path.isfile(ruta):
                    # En Windows Kivy carga mejor con barras normales
                    ruta_carga = ruta.replace('\\', '/')
                    self.sounds['pregunta'] = SoundLoader.load(ruta_carga)
                    break
            if self.sounds['pregunta']:
                break
            for f in sorted(os.listdir(audio_dir)):
                low = f.lower()
                if low.endswith(('.wav', '.ogg', '.mp3')) or 'pregunta' in low or 'question' in low:
                    ruta = os.path.join(audio_dir, f)
                    if os.path.isfile(ruta):
                        ruta_carga = ruta.replace('\\', '/')
                        self.sounds['pregunta'] = SoundLoader.load(ruta_carga)
                        break
            if self.sounds['pregunta']:
                break
        
        for sound in self.sounds.values():
            if sound:
                sound.volume = 0.5

    def cargar_preguntas(self):
        """Carga las preguntas desde archivos JSON."""
        import json
        import random
        
        preguntas_dir = os.path.join(BASE_DIR, 'preguntas')
        if not os.path.exists(preguntas_dir):
            os.makedirs(preguntas_dir)
            self.crear_preguntas_ejemplo()
        
        all_questions = []
        try:
            for archivo in sorted(os.listdir(preguntas_dir)):
                if archivo.endswith('.json'):
                    ruta = os.path.join(preguntas_dir, archivo)
                    with open(ruta, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        preguntas = data.get('preguntas', [])
                        for p in preguntas:
                            p['dificultad'] = data.get('dificultad', 'media')
                        all_questions.extend(preguntas)
        except Exception as e:
            print(f"Error cargando preguntas: {e}")
            all_questions = self.crear_preguntas_ejemplo()
        
        # Mezclar y seleccionar 15 preguntas
        if len(all_questions) >= 15:
            random.shuffle(all_questions)
            self.preguntas = all_questions[:15]
        else:
            while len(self.preguntas) < 15:
                self.preguntas.extend(all_questions)
            self.preguntas = self.preguntas[:15]

    def crear_preguntas_ejemplo(self):
        """Crea preguntas bíblicas de ejemplo si no existen archivos."""
        import json
        
        # Solo un ejemplo mínimo - las preguntas reales están en JSON
        preguntas_ejemplo = {
            "dificultad": "variable",
            "preguntas": [
                {
                    "pregunta": "¿Cuántos días tardó Dios en crear el mundo?",
                    "opciones": ["3 días", "6 días", "7 días", "40 días"],
                    "respuesta_correcta": 1,
                    "nivel": 1
                }
            ]
        }
        
        preguntas_dir = os.path.join(BASE_DIR, 'preguntas')
        os.makedirs(preguntas_dir, exist_ok=True)
        ruta = os.path.join(preguntas_dir, 'preguntas_biblicas.json')
        
        # Solo crear si no existe
        if not os.path.exists(ruta):
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(preguntas_ejemplo, f, ensure_ascii=False, indent=2)
        
        return preguntas_ejemplo.get('preguntas', [])

    # ========== MÉTODOS DEL JUEGO ==========
    # Estos métodos manejan la lógica del juego
    
    def resetear_juego(self):
        """Reinicia el juego a su estado inicial."""
        # Cancelar programación de primera pregunta si existe (evita doble carga/audio)
        if self._schedule_primera_pregunta is not None:
            try:
                self._schedule_primera_pregunta.cancel()
            except Exception:
                pass
            self._schedule_primera_pregunta = None
        # Cancelar timer si existe
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        
        import random
        self.pregunta_indice = 0
        self.comodines_usados = {
            '50/50': False,
            'llamada': False,
            'publico': False,
            'busqueda_biblica': False
        }
        self.premio_actual = 0
        self.premio_seguridad = 0
        self.tiempo_restante = 30
        self.game_in_progress = True
        self._indice_ultima_pregunta_con_audio = -1
        self._sonido_pregunta_playing = False
        if self._sonido_pregunta_stop_event is not None:
            try:
                self._sonido_pregunta_stop_event.cancel()
            except Exception:
                pass
            self._sonido_pregunta_stop_event = None
        if self.sounds.get('pregunta'):
            try:
                self.sounds['pregunta'].stop()
            except Exception:
                pass
        random.shuffle(self.preguntas)

    def cargar_pregunta_actual(self):
        """Carga y muestra la pregunta actual en la pantalla de juego."""
        if self._cargando_pregunta_actual:
            return
        # Fallback: si el hilo aún no terminó (carpeta compartida lenta), cargar aquí
        if not self.preguntas and self.pregunta_indice == 0:
            try:
                self.cargar_preguntas()
            except Exception:
                pass
        if not self.game_in_progress or self.pregunta_indice >= len(self.preguntas):
            self.finalizar_juego()
            return

        self._cargando_pregunta_actual = True
        try:
            self._cargar_pregunta_actual_impl()
        finally:
            self._cargando_pregunta_actual = False

    def reproducir_sonido_pregunta_una_vez(self):
        """Reproduce el sonido de pregunta una sola vez. No vuelve a iniciar si ya está sonando."""
        if self._sonido_pregunta_playing:
            return
        snd = self.sounds.get('pregunta')
        if not snd:
            return
        # Cancelar cualquier stop programado anterior
        if self._sonido_pregunta_stop_event is not None:
            try:
                self._sonido_pregunta_stop_event.cancel()
            except Exception:
                pass
            self._sonido_pregunta_stop_event = None
        self._sonido_pregunta_playing = True
        try:
            snd.stop()
        except Exception:
            pass
        snd.play()
        # Detener tras la duración del archivo (una sola pasada) o a 10 s si no se conoce (evita loop infinito)
        dur = 10.0
        try:
            L = getattr(snd, 'length', 0) or 0
            if L > 0:
                dur = L + 0.3
        except Exception:
            pass

        def _parar_sonido(dt):
            self._sonido_pregunta_playing = False
            self._sonido_pregunta_stop_event = None
            if snd:
                try:
                    snd.stop()
                except Exception:
                    pass

        self._sonido_pregunta_stop_event = Clock.schedule_once(_parar_sonido, dur)

    def _cargar_pregunta_actual_impl(self):
        """Implementación interna: solo actualiza UI, no reproduce audio."""
        self.pregunta_actual = self.preguntas[self.pregunta_indice]
        game_screen = self.sm.get_screen('juego')
        
        # Cancelar timer anterior si existe
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        
        # Reiniciar tiempo
        self.tiempo_restante = 30
        
        if game_screen:
            # Actualizar pregunta
            if hasattr(game_screen.ids, 'pregunta_text'):
                game_screen.ids.pregunta_text.text = self.pregunta_actual['pregunta']
            
            # Actualizar opciones
            opciones = self.pregunta_actual['opciones']
            letras = ['a', 'b', 'c', 'd']
            
            for i, letra in enumerate(letras):
                label_id = f'opcion_{letra}'
                card_id = f'opcion_{letra}_card'
                if hasattr(game_screen.ids, label_id):
                    label = getattr(game_screen.ids, label_id)
                    label.text = opciones[i]
                if hasattr(game_screen.ids, card_id):
                    card = getattr(game_screen.ids, card_id)
                    card.md_bg_color = (0.1, 0.1, 0.3, 1)
                    card.opacity = 1
                    card.disabled = False
            
            # Actualizar nivel (solo número)
            nivel = self.pregunta_indice + 1
            if hasattr(game_screen.ids, 'nivel_text'):
                game_screen.ids.nivel_text.text = str(nivel)
            
            # Actualizar timer
            if hasattr(game_screen.ids, 'timer_text'):
                game_screen.ids.timer_text.text = str(self.tiempo_restante)
                game_screen.ids.timer_text.text_color = (1, 0.2, 0.2, 1) if self.tiempo_restante <= 10 else (1, 1, 1, 1)
            
            # Actualizar lista de premios y comodines
            self.actualizar_lista_premios()
            self.actualizar_comodines()
            self.cargar_imagenes_comodines()
            
            # Iniciar contador
            self.iniciar_timer()

    def actualizar_lista_premios(self):
        """Actualiza la escalera de premios en la UI (15 niveles visibles, sin amontonar)."""
        game_screen = self.sm.get_screen('juego')
        if not game_screen or not hasattr(game_screen.ids, 'premios_list'):
            return
        
        premios_list = game_screen.ids.premios_list
        premios_list.clear_widgets()
        
        # Mostrar los 15 niveles completos
        niveles_mostrar = 15
        for i in range(niveles_mostrar):
            nivel = i + 1
            if nivel <= len(PREMIOS):
                premio = PREMIOS[nivel - 1]
            else:
                premio = "$0"
            
            is_current = nivel == (self.pregunta_indice + 1)
            is_passed = nivel <= self.pregunta_indice
            is_seguro = nivel in SEGURIDAD
            
            # Colores según estado
            if is_current:
                text_color = (1, 1, 1, 1)
                bg_color = (0.2, 0.2, 0.4, 1)
                border_color = (1, 1, 1, 1)
            elif is_passed:
                text_color = (0.5, 0.5, 0.5, 1)
                bg_color = (0.1, 0.1, 0.2, 0.5)
                border_color = (0.3, 0.3, 0.3, 0.5)
            else:
                text_color = (1, 1, 1, 0.7)
                bg_color = (0.1, 0.1, 0.2, 0.3)
                border_color = (0.5, 0.5, 0.5, 0.3)
            
            # Contenedor compacto por nivel (altura fija para que quepan los 15)
            box = MDBoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height="26dp",
                spacing="3dp",
                padding="2dp"
            )
            
            # Número de nivel
            numero_label = MDLabel(
                text=f"◆{nivel}" if nivel <= 9 else str(nivel),
                theme_text_color="Custom",
                text_color=border_color if is_current else text_color,
                font_style="Caption",
                font_size="12sp",
                size_hint_x=None,
                width="24dp",
                halign="center"
            )
            
            # Premio (texto corto en niveles altos para no amontonar)
            premio_label = MDLabel(
                text=premio,
                theme_text_color="Custom",
                text_color=text_color,
                font_style="Caption",
                font_size="11sp",
                halign="left",
                bold=is_current
            )
            
            # Etiquetas de seguridad (preguntas 5 y 10)
            if is_seguro:
                seguro_text = "Seguro 1" if nivel == SEGURIDAD[0] else "Seguro 2"
                seguro_label = MDLabel(
                    text=seguro_text,
                    theme_text_color="Custom",
                    text_color=(1, 0.84, 0, 1),
                    font_style="Caption",
                    font_size="9sp",
                    size_hint_x=None,
                    width="52dp",
                    halign="left"
                )
                box.add_widget(seguro_label)
            
            if nivel == 15:
                premio_label.text = "Premio"
            
            box.add_widget(numero_label)
            box.add_widget(premio_label)
            
            # Card por nivel
            card = MDCard(
                md_bg_color=bg_color,
                padding="2dp",
                size_hint_y=None,
                height="26dp",
                elevation=3 if is_current else 0,
                radius=[4, 4, 4, 4]
            )
            card.add_widget(box)
            premios_list.add_widget(card)

    def actualizar_comodines(self):
        """Actualiza el estado visual de los comodines."""
        game_screen = self.sm.get_screen('juego')
        if not game_screen:
            return
        
        if hasattr(game_screen.ids, 'comodin_50_50'):
            btn = game_screen.ids.comodin_50_50
            usado = self.comodines_usados.get('50/50', False)
            btn.disabled = usado
            btn.opacity = 0.3 if usado else 1
        
        if hasattr(game_screen.ids, 'comodin_publico'):
            btn = game_screen.ids.comodin_publico
            usado = self.comodines_usados.get('publico', False)
            btn.disabled = usado
            btn.opacity = 0.3 if usado else 1

        if hasattr(game_screen.ids, 'comodin_busqueda_biblica'):
            btn = game_screen.ids.comodin_busqueda_biblica
            usado = self.comodines_usados.get('busqueda_biblica', False)
            btn.disabled = usado
            btn.opacity = 0.3 if usado else 1

    def cargar_imagenes_comodines(self):
        """Carga las imágenes de los comodines desde assets/comodines o comodines del proyecto."""
        game_screen = self.sm.get_screen('juego')
        if not game_screen:
            return
        for id_boton, nombre_archivo in IMAGENES_COMODINES:
            if not hasattr(game_screen.ids, id_boton):
                continue
            ruta = None
            for carpeta in COMODINES_DIRS:
                candidata = os.path.join(carpeta, nombre_archivo)
                if os.path.isfile(candidata):
                    ruta = candidata
                    break
            if ruta:
                try:
                    game_screen.ids[id_boton].source = ruta
                except Exception:
                    pass

    def iniciar_timer(self):
        """Inicia el contador de 30 segundos."""
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.actualizar_timer, 1.0)
    
    def actualizar_timer(self, dt):
        """Actualiza el contador cada segundo."""
        self.tiempo_restante -= 1
        game_screen = self.sm.get_screen('juego')
        
        if game_screen and hasattr(game_screen.ids, 'timer_text'):
            game_screen.ids.timer_text.text = str(self.tiempo_restante)
            if self.tiempo_restante <= 10:
                game_screen.ids.timer_text.text_color = (1, 0.2, 0.2, 1)
            else:
                game_screen.ids.timer_text.text_color = (1, 1, 1, 1)
        
        if self.tiempo_restante <= 0:
            if self.timer_event:
                self.timer_event.cancel()
                self.timer_event = None
            self.procesar_respuesta_tiempo_agotado()
    
    def procesar_respuesta_tiempo_agotado(self):
        """Procesa cuando se agota el tiempo."""
        if not self.pregunta_actual:
            return
        
        game_screen = self.sm.get_screen('juego')
        letras = ['a', 'b', 'c', 'd']
        for letra in letras:
            card_id = f'opcion_{letra}_card'
            if hasattr(game_screen.ids, card_id):
                card = getattr(game_screen.ids, card_id)
                card.disabled = True
        
        correcta = self.pregunta_actual['respuesta_correcta']
        if hasattr(game_screen.ids, f'opcion_{letras[correcta]}_card'):
            card_correcta = getattr(game_screen.ids, f'opcion_{letras[correcta]}_card')
            card_correcta.md_bg_color = (0.15, 0.75, 0.15, 1)  # Verde bien visible
        if self.sounds.get('wrong'):
            self.sounds['wrong'].play()
        
        if hasattr(game_screen.ids, 'timer_text'):
            game_screen.ids.timer_text.text = "0"
            game_screen.ids.timer_text.text_color = (1, 0.2, 0.2, 1)
        
        Clock.schedule_once(lambda dt: self.finalizar_juego(ganador=False), 2.0)
    
    def procesar_respuesta(self, indice):
        """Procesa la respuesta del jugador."""
        if not self.pregunta_actual:
            return
        
        # Cancelar timer si el usuario respondió
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        
        # Deshabilitar todas las opciones
        game_screen = self.sm.get_screen('juego')
        letras = ['a', 'b', 'c', 'd']
        for letra in letras:
            card_id = f'opcion_{letra}_card'
            if hasattr(game_screen.ids, card_id):
                card = getattr(game_screen.ids, card_id)
                card.disabled = True
        
        correcta = self.pregunta_actual['respuesta_correcta']
        es_correcta = indice == correcta
        
        # Resaltar respuestas: correcta en verde, incorrecta elegida en rojo
        if hasattr(game_screen.ids, f'opcion_{letras[correcta]}_card'):
            card_correcta = getattr(game_screen.ids, f'opcion_{letras[correcta]}_card')
            card_correcta.md_bg_color = (0.15, 0.75, 0.15, 1)  # Verde
        if not es_correcta and hasattr(game_screen.ids, f'opcion_{letras[indice]}_card'):
            card_incorrecta = getattr(game_screen.ids, f'opcion_{letras[indice]}_card')
            card_incorrecta.md_bg_color = (0.85, 0.15, 0.15, 1)  # Rojo
        
        # Reproducir sonido
        if es_correcta and self.sounds.get('correct'):
            self.sounds['correct'].play()
        elif not es_correcta and self.sounds.get('wrong'):
            self.sounds['wrong'].play()
        
        if es_correcta:
            def siguiente_pregunta(dt):
                self.pregunta_indice += 1
                if self.pregunta_indice <= len(PREMIOS):
                    self.premio_actual = self.pregunta_indice
                if (self.pregunta_indice) in SEGURIDAD:
                    self.premio_seguridad = self.pregunta_indice
                # Sonido solo aquí, una vez por pregunta (nunca dentro de cargar_pregunta_actual)
                self.reproducir_sonido_pregunta_una_vez()
                self.cargar_pregunta_actual()
            Clock.schedule_once(siguiente_pregunta, 2.0)
        else:
            Clock.schedule_once(lambda dt: self.finalizar_juego(ganador=False), 2.0)

    def usar_comodin(self, tipo):
        """Usa un comodín."""
        if self.comodines_usados.get(tipo, True):
            return
        
        self.comodines_usados[tipo] = True
        game_screen = self.sm.get_screen('juego')
        
        if tipo == '50/50':
            self.comodin_50_50()
        elif tipo == 'llamada':
            self.comodin_llamada()
        elif tipo == 'publico':
            self.comodin_publico()
        elif tipo == 'busqueda_biblica':
            self.comodin_busqueda_biblica()
        
        self.actualizar_comodines()

    def comodin_50_50(self):
        """Elimina 2 opciones incorrectas."""
        if not self.pregunta_actual:
            return
        
        import random
        correcta = self.pregunta_actual['respuesta_correcta']
        opciones_incorrectas = [i for i in range(4) if i != correcta]
        eliminar = random.sample(opciones_incorrectas, 2)
        
        game_screen = self.sm.get_screen('juego')
        letras = ['a', 'b', 'c', 'd']
        
        for i in eliminar:
            card_id = f'opcion_{letras[i]}_card'
            if hasattr(game_screen.ids, card_id):
                card = getattr(game_screen.ids, card_id)
                card.opacity = 0.3
                card.disabled = True

    def comodin_llamada(self):
        """Muestra una ayuda (pista)."""
        if not self.pregunta_actual:
            return
        
        import random
        correcta = self.pregunta_actual['respuesta_correcta']
        opciones = self.pregunta_actual['opciones']
        letra_correcta = chr(65 + correcta)
        
        pistas = [
            f"Tu amigo sugiere que podría ser la opción {letra_correcta}",
            f"La respuesta parece ser {letra_correcta}",
            f"Probablemente es {opciones[correcta]}"
        ]
        
        pista = random.choice(pistas)
        dialog = MDDialog(
            title="Llamada a un amigo",
            text=pista,
            buttons=[
                MDRaisedButton(
                    text="Entendido",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def comodin_publico(self):
        """Muestra los resultados de la votación del público."""
        if not self.pregunta_actual:
            return
        
        import random
        correcta = self.pregunta_actual['respuesta_correcta']
        
        porcentajes = [0] * 4
        porcentajes[correcta] = random.randint(45, 70)
        
        restante = 100 - porcentajes[correcta]
        otros = [i for i in range(4) if i != correcta]
        random.shuffle(otros)
        
        for i in otros:
            if restante > 0:
                porcentajes[i] = random.randint(0, min(30, restante))
                restante -= porcentajes[i]
        
        porcentajes[otros[-1]] += restante
        
        letras = ['A', 'B', 'C', 'D']
        resultado_text = "Resultados de la votación del público:\n\n"
        for i, letra in enumerate(letras):
            resultado_text += f"{letra}: {porcentajes[i]}%\n"
        
        dialog = MDDialog(
            title="Consulta al público",
            text=resultado_text,
            buttons=[
                MDRaisedButton(
                    text="Entendido",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def comodin_busqueda_biblica(self):
        """Muestra la cita bíblica donde se encuentra la respuesta."""
        if not self.pregunta_actual:
            return

        cita = self.pregunta_actual.get(
            'cita_biblica',
            'Consulta tu Biblia para encontrar la respuesta a esta pregunta.'
        )
        dialog = MDDialog(
            title="Búsqueda bíblica",
            text=f"La respuesta se encuentra en:\n\n{cita}",
            buttons=[
                MDRaisedButton(
                    text="Entendido",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def finalizar_juego(self, ganador=True):
        """Finaliza el juego y muestra el resultado."""
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        
        self.game_in_progress = False
        
        # Determinar premio final
        if ganador:
            premio_final = PREMIOS[-1]
            mensaje = "¡FELICIDADES! ¡ERES MILLONARIO!"
        else:
            if self.pregunta_indice >= SEGURIDAD[1]:
                premio_final = PREMIOS[SEGURIDAD[1] - 1]
            elif self.pregunta_indice >= SEGURIDAD[0]:
                premio_final = PREMIOS[SEGURIDAD[0] - 1]
            else:
                premio_final = "$0"
            mensaje = f"Juego terminado. Ganaste: {premio_final}"
        
        # Mostrar diálogo de resultado
        content = MDBoxLayout(
            orientation='vertical',
            spacing='10dp',
            padding='10dp',
            size_hint_y=None,
            height='200dp'
        )
        
        label = MDLabel(
            text=mensaje + f"\n\nPremio final: {premio_final}",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 0.84, 0, 1) if ganador else (1, 1, 1, 1),
            font_style="H5"
        )
        content.add_widget(label)
        
        dialog = MDDialog(
            title="Fin del Juego",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="Nuevo Juego",
                    on_release=lambda x: self.nuevo_juego(dialog)
                ),
                MDFlatButton(
                    text="Salir",
                    on_release=lambda x: self.salir_juego(dialog)
                )
            ],
        )
        dialog.open()

    def nuevo_juego(self, dialog):
        """Inicia un nuevo juego."""
        if dialog:
            dialog.dismiss()
        self.cambiar_pantalla('menu', 'right')

    def salir_juego(self, dialog):
        """Sale al menú principal."""
        if dialog:
            dialog.dismiss()
        self.cambiar_pantalla('menu', 'right')

    def cambiar_pantalla(self, nombre_pantalla, direccion='left'):
        """Cambia de pantalla con animación."""
        if not self.sm:
            return
        
        if direccion == 'left':
            self.sm.transition = SlideTransition(direction='left')
        elif direccion == 'right':
            self.sm.transition = SlideTransition(direction='right')
        elif direccion == 'up':
            self.sm.transition = SlideTransition(direction='up')
        else:
            self.sm.transition = FadeTransition()
        
        self.sm.current = nombre_pantalla


if __name__ == '__main__':
    MillonarioApp().run()
