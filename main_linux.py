#!/usr/bin/env python3
"""
Punto de entrada para Linux (Ubuntu, VirtualBox, carpetas compartidas).

Configura X11, carga preguntas en hilo. Por defecto NO carga audio en Linux
para evitar que la app se quede pegada ("not responding" / "Killed").
Para intentar con audio: KIVY_SKIP_AUDIO=0 ./run_app_local.sh

Uso: python3 main_linux.py   o   ./run_app.sh
"""
import os as _os
import threading

# Antes de importar Kivy: solo en Linux
_os.environ.setdefault("SDL_VIDEODRIVER", "x11")
_os.environ.setdefault("GDK_BACKEND", "x11")
_os.environ.setdefault("KIVY_GL_BACKEND", "sdl2")
_os.environ.setdefault("KIVY_CLIPBOARD", "sdl2")
# Sin audio por defecto en Linux para no bloquear la ventana (carpeta compartida / VM)
_os.environ.setdefault("KIVY_SKIP_AUDIO", "1")

from kivy.core.audio import SoundLoader
from kivy.clock import Clock

# Importar la app y constantes del proyecto común
from main import MillonarioApp, BASE_DIR, AUDIOS_DIRS


def _load_preguntas_en_hilo(base_dir):
    """Carga preguntas desde JSON en un hilo. Devuelve lista de hasta 15."""
    import json
    import random
    import os
    preguntas_dir = os.path.join(base_dir, 'preguntas')
    if not os.path.exists(preguntas_dir):
        try:
            os.makedirs(preguntas_dir, exist_ok=True)
            ruta = os.path.join(preguntas_dir, 'preguntas_biblicas.json')
            if not os.path.exists(ruta):
                ej = {
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
                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump(ej, f, ensure_ascii=False, indent=2)
        except Exception:
            return []

    all_questions = []
    try:
        for archivo in sorted(os.listdir(preguntas_dir)):
            if not archivo.endswith('.json'):
                continue
            ruta = os.path.join(preguntas_dir, archivo)
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                preguntas = data.get('preguntas', [])
                dificultad = data.get('dificultad', 'media')
                for p in preguntas:
                    p['dificultad'] = dificultad
                all_questions.extend(preguntas)
    except Exception:
        return []

    if len(all_questions) >= 15:
        random.shuffle(all_questions)
        return all_questions[:15]
    out = []
    while len(out) < 15:
        out.extend(all_questions)
    return out[:15]


def _load_sonidos_en_hilo(base_dir, audios_dirs):
    """Carga sonidos en un hilo. Devuelve dict 'click', 'correct', 'wrong', 'pregunta'."""
    import os
    sounds_dir = os.path.join(base_dir, 'sounds')
    out = {
        'click': SoundLoader.load(os.path.join(sounds_dir, 'click.wav')),
        'correct': SoundLoader.load(os.path.join(sounds_dir, 'correct.wav')),
        'wrong': SoundLoader.load(os.path.join(sounds_dir, 'wrong.wav')),
        'pregunta': None,
    }
    nombres_preferidos = ['audio editado_pregunta.mp3', 'pregunta.wav', 'pregunta.ogg', 'question.wav', 'question.ogg']
    for audio_dir in audios_dirs:
        if not os.path.isdir(audio_dir):
            continue
        for nombre in nombres_preferidos:
            ruta = os.path.join(audio_dir, nombre)
            if os.path.isfile(ruta):
                out['pregunta'] = SoundLoader.load(ruta.replace('\\', '/'))
                break
        if out['pregunta']:
            break
        try:
            for f in sorted(os.listdir(audio_dir)):
                low = f.lower()
                if low.endswith(('.wav', '.ogg', '.mp3')) or 'pregunta' in low or 'question' in low:
                    ruta = os.path.join(audio_dir, f)
                    if os.path.isfile(ruta):
                        out['pregunta'] = SoundLoader.load(ruta.replace('\\', '/'))
                        break
                if out['pregunta']:
                    break
        except Exception:
            pass
        if out['pregunta']:
            break
    return out


class MillonarioAppLinux(MillonarioApp):
    """Versión Linux: carga preguntas y sonidos en hilos para no bloquear la GUI."""

    def _cargar_recursos(self, dt):
        def _thread_preguntas():
            try:
                result = _load_preguntas_en_hilo(BASE_DIR)
                Clock.schedule_once(lambda d: self._asignar_preguntas(result), 0)
            except Exception as e:
                print(f"[Millonario] Error cargando preguntas: {e}")
                Clock.schedule_once(lambda d: self._asignar_preguntas([]), 0)
        threading.Thread(target=_thread_preguntas, daemon=True).start()

        # En Linux por defecto KIVY_SKIP_AUDIO=1 para no bloquear; si está a 0, cargar en hilo más tarde
        if _os.environ.get("KIVY_SKIP_AUDIO"):
            return
        Clock.schedule_once(self._iniciar_carga_sonidos_en_hilo, 15.0)

    def _asignar_preguntas(self, lista):
        if lista:
            self.preguntas = lista
        elif not self.preguntas:
            try:
                self.cargar_preguntas()
            except Exception as e:
                print(f"[Millonario] Fallback cargar_preguntas: {e}")

    def _iniciar_carga_sonidos_en_hilo(self, dt):
        def _thread():
            try:
                sounds_dict = _load_sonidos_en_hilo(BASE_DIR, AUDIOS_DIRS)
                Clock.schedule_once(lambda d: self._asignar_sonidos(sounds_dict), 0)
            except Exception as e:
                print(f"[Millonario] Error cargando sonidos (la app sigue sin audio): {e}")
        threading.Thread(target=_thread, daemon=True).start()

    def _asignar_sonidos(self, sounds_dict):
        if sounds_dict:
            self.sounds.update(sounds_dict)
            for s in self.sounds.values():
                if s:
                    try:
                        s.volume = 0.5
                    except Exception:
                        pass


if __name__ == '__main__':
    MillonarioAppLinux().run()
