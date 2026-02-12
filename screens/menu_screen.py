"""
Pantalla del menú principal
"""
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock


class MenuScreen(MDScreen):
    """Pantalla principal del menú con opciones de juego."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'menu'

    def iniciar_juego(self):
        """Inicia un nuevo juego."""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and hasattr(app, 'resetear_juego'):
            app.resetear_juego()
            app.cambiar_pantalla('juego', 'left')
            # Sonido + carga de la primera pregunta una sola vez (el sonido solo se toca aquí para la 1ª)
            def _primera_pregunta(dt):
                app._schedule_primera_pregunta = None
                if hasattr(app, 'reproducir_sonido_pregunta_una_vez'):
                    app.reproducir_sonido_pregunta_una_vez()
                if hasattr(app, 'cargar_pregunta_actual'):
                    app.cargar_pregunta_actual()
            app._schedule_primera_pregunta = Clock.schedule_once(_primera_pregunta, 0.15)

    def mostrar_instrucciones(self):
        """Muestra un diálogo con las instrucciones del juego."""
        instructions = """
¿QUIÉN QUIERE SER MILLONARIO?
BÍBLICO

REGLAS DEL JUEGO:
• Responde 15 preguntas bíblicas
• Cada pregunta tiene 4 opciones
• Puedes usar 4 comodines:
  - 50/50: Elimina 2 respuestas incorrectas
  - Llamada: Te ayuda con una respuesta
  - Público: La audiencia vota
  - Búsqueda bíblica: Muestra la cita donde está la respuesta

NIVELES DE SEGURIDAD:
• Pregunta 5: $1,000 garantizado
• Pregunta 10: $32,000 garantizado

¡Buena suerte!
        """
        dialog = MDDialog(
            title="Instrucciones",
            text=instructions,
            buttons=[
                MDRaisedButton(
                    text="Cerrar",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

