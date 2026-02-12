"""
Lógica del juego: manejo de preguntas, respuestas y comodines
"""
import os
import json
import random
from config import PREMIOS, SEGURIDAD


class GameLogic:
    """Clase que maneja toda la lógica del juego."""
    
    def __init__(self):
        self.preguntas = []
        self.pregunta_actual = None
        self.pregunta_indice = 0
        self.comodines_usados = {
            '50/50': False,
            'llamada': False,
            'publico': False
        }
        self.premio_actual = 0
        self.premio_seguridad = 0
        self.game_in_progress = False

    def cargar_preguntas(self):
        """Carga preguntas desde archivos JSON."""
        preguntas_dir = 'preguntas'
        if not os.path.exists(preguntas_dir):
            os.makedirs(preguntas_dir)
            self.crear_preguntas_ejemplo()
        
        all_questions = []
        try:
            for archivo in os.listdir(preguntas_dir):
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
        
        # Mezclar preguntas y seleccionar 15
        if len(all_questions) >= 15:
            random.shuffle(all_questions)
            self.preguntas = all_questions[:15]
        else:
            while len(self.preguntas) < 15:
                self.preguntas.extend(all_questions)
            self.preguntas = self.preguntas[:15]

    def crear_preguntas_ejemplo(self):
        """Crea preguntas bíblicas de ejemplo si no existen archivos."""
        preguntas_ejemplo = {
            "dificultad": "variable",
            "preguntas": [
                {
                    "pregunta": "¿Cuántos días tardó Dios en crear el mundo?",
                    "opciones": ["3 días", "6 días", "7 días", "40 días"],
                    "respuesta_correcta": 1,
                    "nivel": 1
                },
                {
                    "pregunta": "¿Cuál fue el primer hombre creado por Dios?",
                    "opciones": ["Noé", "Adán", "Abraham", "Moisés"],
                    "respuesta_correcta": 1,
                    "nivel": 1
                },
            ]
        }
        
        preguntas_dir = 'preguntas'
        os.makedirs(preguntas_dir, exist_ok=True)
        with open(os.path.join(preguntas_dir, 'preguntas_biblicas.json'), 'w', encoding='utf-8') as f:
            json.dump(preguntas_ejemplo, f, ensure_ascii=False, indent=2)
        
        return preguntas_ejemplo.get('preguntas', [])

    def resetear_juego(self):
        """Reinicia el juego a su estado inicial."""
        self.pregunta_indice = 0
        self.comodines_usados = {
            '50/50': False,
            'llamada': False,
            'publico': False
        }
        self.premio_actual = 0
        self.premio_seguridad = 0
        self.game_in_progress = True
        random.shuffle(self.preguntas)

    def obtener_premio_seguridad(self, pregunta_indice):
        """Obtiene el premio de seguridad según el nivel alcanzado."""
        if pregunta_indice >= SEGURIDAD[1]:  # Nivel 10
            return PREMIOS[SEGURIDAD[1] - 1]  # $32,000
        elif pregunta_indice >= SEGURIDAD[0]:  # Nivel 5
            return PREMIOS[SEGURIDAD[0] - 1]  # $1,000
        return "$0"


