"""
Pantalla de carga (Splash Screen)
"""
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
import random
from config import VERSICULOS_BIBLICOS


class SplashScreen(MDScreen):
    """Pantalla de carga con barra de progreso y versículos bíblicos."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progress = 0
        self.progress_event = None
        self.versiculos = VERSICULOS_BIBLICOS

    def on_enter(self):
        """Se llama cuando entra la pantalla: inicia la animación de carga."""
        self.progress = 0
        if self.progress_event:
            self.progress_event.cancel()
            self.progress_event = None

        self._actualizar_versiculo()
        self._actualizar_barra()

        # Actualizar progreso cada 0.08 segundos aprox. (unos 8 segundos en total)
        self.progress_event = Clock.schedule_interval(self._actualizar_carga, 0.08)

    def on_leave(self, *args):
        """Detiene el timer si se sale de la pantalla."""
        if self.progress_event:
            self.progress_event.cancel()
            self.progress_event = None

    def _actualizar_barra(self):
        """Refresca el valor de la barra de progreso y el porcentaje."""
        if hasattr(self.ids, "progress_bar"):
            self.ids.progress_bar.value = self.progress
        if hasattr(self.ids, "loading_percent"):
            self.ids.loading_percent.text = f"{int(self.progress)}%"

    def _actualizar_versiculo(self):
        """Muestra un versículo bíblico aleatorio en la etiqueta."""
        if not self.versiculos:
            return
        texto = random.choice(self.versiculos)
        if hasattr(self.ids, "versiculo_text"):
            self.ids.versiculo_text.text = texto

    def _actualizar_carga(self, dt):
        """Incrementa la barra de progreso hasta llegar al menú."""
        self.progress += 2
        if self.progress >= 100:
            self.progress = 100
            self._actualizar_barra()
            if self.progress_event:
                self.progress_event.cancel()
                self.progress_event = None
            self.ir_a_menu()
            return False  # Detener el schedule_interval

        # Actualizar UI
        self._actualizar_barra()

        # Cambiar versículo cada 25%
        if self.progress % 25 == 0:
            self._actualizar_versiculo()

        return True

    def ir_a_menu(self, *args):
        """Cambia a la pantalla del menú principal."""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and hasattr(app, "sm") and app.sm:
            app.sm.current = "menu"

