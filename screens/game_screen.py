"""
Pantalla del juego principal
"""
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock


class GameScreen(MDScreen):
    """Pantalla principal del juego donde se muestran las preguntas."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'juego'
        self.respuesta_seleccionada = None

    def on_enter(self):
        """Se llama cuando se entra a la pantalla de juego. La primera pregunta se carga desde el menú para que el audio suene solo una vez."""
        pass

    def seleccionar_respuesta(self, indice):
        """Maneja la selección de una respuesta por el usuario."""
        from kivymd.app import MDApp
        self.respuesta_seleccionada = indice
        app = MDApp.get_running_app()
        if app and hasattr(app, 'procesar_respuesta'):
            app.procesar_respuesta(indice)

    def usar_comodin(self, tipo):
        """Maneja el uso de un comodín."""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and hasattr(app, 'usar_comodin'):
            app.usar_comodin(tipo)
    
    def mostrar_feedback(self, mensaje, correcto):
        """Muestra feedback visual temporal al usuario."""
        dialog = MDDialog(
            title="¡Correcto!" if correcto else "Incorrecto",
            text=mensaje,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()
        # Auto cerrar después de 1.5 segundos
        Clock.schedule_once(lambda dt: dialog.dismiss(), 1.5)

