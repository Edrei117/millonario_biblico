# Script para agregar cita_biblica a cada pregunta (ejecutar una vez)
import json
import os

RUTA = os.path.join(os.path.dirname(__file__), 'preguntas', 'preguntas_biblicas.json')

# Citas en orden de las preguntas del JSON actual
CITAS = [
    "Génesis 1 (creación en 6 días)",
    "Génesis 2:7 (Adán)",
    "Génesis 2:21-22 (Eva)",
    "Génesis 2-3 (Eva)",
    "Génesis 3 (fruto prohibido)",
    "Libro de Jonás",
    "Génesis 6-9 (Noé y el arca)",
    "Génesis 7:12 (40 días de lluvia)",
    "Mateo 10:2-4 / Lucas 6:13-16 (12 discípulos)",
    "Mateo 26:48-49 (Judas)",
    "Juan 2:1-11 (bodas de Caná)",
    "Éxodo 20 (10 mandamientos)",
    "Éxodo 20 (los 10 mandamientos)",
    "1 Reyes 3 (Salomón)",
    "Lucas 3:23 (Jesús ~30 años)",
    "Cartas de Pablo en el NT",
    "Apocalipsis (último libro)",
    "27 libros (2 Pedro, etc.)",
    "Lucas 1:13 (Zacarías)",
    "Miqueas 5:2 / Mateo 2:1 (Belén)",
    "66 libros (canon)",
    "1 Samuel 9-10 (Saúl)",
    "Daniel 6 (Daniel en el foso)",
    "Santiago 2:23 (Abraham amigo de Dios)",
    "Mateo 3:13 (río Jordán)",
    "Hechos 7 (Esteban)",
    "Génesis 5:27 (Matusalén 969 años)",
    "Juan 18:15-27 (Pedro niega)",
    "Proverbios (Salomón)",
    "73 Salmos de David (tradición)",
    "Éxodo 19-20 (Monte Sinaí)",
    "Mateo 4:18 (Pedro pescador)",
    "Isaías 7:14 / 9:6",
    "Mateo 4:2 / Lucas 4:2 (40 días)",
    "Isaías 7:14 (Emmanuel)",
    "Jueces 16 (Sansón y Dalila)",
    "Daniel 4 (Nabucodonosor)",
]

with open(RUTA, 'r', encoding='utf-8') as f:
    data = json.load(f)

preguntas = data['preguntas']
for i, p in enumerate(preguntas):
    p['cita_biblica'] = CITAS[i] if i < len(CITAS) else "Consulta tu Biblia para esta pregunta."

with open(RUTA, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Citas bíblicas agregadas correctamente.")
