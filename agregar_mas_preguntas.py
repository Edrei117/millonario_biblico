# Agregar ~52 preguntas más para llegar a ~235 total
import json
import os

RUTA = os.path.join(os.path.dirname(__file__), 'preguntas', 'preguntas_biblicas.json')

MAS = [
    {"pregunta": "¿Quién fue la madre de Samuel?", "opciones": ["Raquel", "Ana", "Ester", "Rut"], "respuesta_correcta": 1, "nivel": 1, "cita_biblica": "1 Samuel 1"},
    {"pregunta": "¿En qué libro está la parábola del buen samaritano?", "opciones": ["Mateo", "Marcos", "Lucas", "Juan"], "respuesta_correcta": 2, "nivel": 2, "cita_biblica": "Lucas 10:25-37"},
    {"pregunta": "¿Cuántos hombres tuvo Gedeón para luchar?", "opciones": ["300", "32.000", "10.000", "1.000"], "respuesta_correcta": 0, "nivel": 4, "cita_biblica": "Jueces 7"},
    {"pregunta": "¿Qué instrumento tocaba David?", "opciones": ["Flauta", "Arpa", "Lira", "Cítara"], "respuesta_correcta": 2, "nivel": 5, "cita_biblica": "1 Samuel 16:23"},
    {"pregunta": "¿Quién fue el profeta que sanó a Naamán?", "opciones": ["Elías", "Eliseo", "Samuel", "Natán"], "respuesta_correcta": 1, "nivel": 6, "cita_biblica": "2 Reyes 5"},
    {"pregunta": "¿En qué ciudad predicó Pablo y fundó iglesias?", "opciones": ["Solo Roma", "Corinto y Éfeso", "Varias ciudades", "Solo Jerusalén"], "respuesta_correcta": 2, "nivel": 7, "cita_biblica": "Hechos"},
    {"pregunta": "¿Cuántos hermanos tenía José?", "opciones": ["10", "11", "12", "9"], "respuesta_correcta": 1, "nivel": 8, "cita_biblica": "Génesis 37"},
    {"pregunta": "¿Qué rey hizo oro como piedras en Jerusalén?", "opciones": ["David", "Salomón", "Ezequías", "Josías"], "respuesta_correcta": 1, "nivel": 9, "cita_biblica": "2 Crónicas 1:15"},
    {"pregunta": "¿Quién fue el primer rey de la dinastía davídica?", "opciones": ["Saúl", "David", "Salomón", "Roboam"], "respuesta_correcta": 1, "nivel": 10, "cita_biblica": "2 Samuel 5"},
    {"pregunta": "¿En qué montaña Abraham iba a sacrificar a Isaac?", "opciones": ["Sinaí", "Moria", "Carmelo", "Tabor"], "respuesta_correcta": 1, "nivel": 11, "cita_biblica": "Génesis 22:2"},
    {"pregunta": "¿Qué apóstol reemplazó a Judas?", "opciones": ["Pablo", "Matías", "Bernabé", "Timoteo"], "respuesta_correcta": 1, "nivel": 12, "cita_biblica": "Hechos 1:26"},
    {"pregunta": "¿Cuántos años tenía Abraham cuando nació Isaac?", "opciones": ["90", "100", "120", "99"], "respuesta_correcta": 1, "nivel": 13, "cita_biblica": "Génesis 21:5"},
    {"pregunta": "¿Quién fue la madre de Salomón?", "opciones": ["Mical", "Betsabé", "Abigail", "Ahinoam"], "respuesta_correcta": 1, "nivel": 14, "cita_biblica": "2 Samuel 12:24"},
    {"pregunta": "¿Qué ave alimentó a Elías en el arroyo?", "opciones": ["Paloma", "Cuervos", "Águila", "Golondrina"], "respuesta_correcta": 1, "nivel": 15, "cita_biblica": "1 Reyes 17:6"},
    {"pregunta": "¿Quién escribió la carta a los Romanos?", "opciones": ["Pedro", "Pablo", "Juan", "Santiago"], "respuesta_correcta": 1, "nivel": 1, "cita_biblica": "Romanos 1:1"},
    {"pregunta": "¿Cuántos capítulos tiene el libro de Génesis?", "opciones": ["40", "50", "60", "45"], "respuesta_correcta": 1, "nivel": 2, "cita_biblica": "Génesis"},
    {"pregunta": "¿Quién fue el rey que vio la escritura en la pared?", "opciones": ["Nabucodonosor", "Belsasar", "Darío", "Ciro"], "respuesta_correcta": 1, "nivel": 3, "cita_biblica": "Daniel 5"},
    {"pregunta": "¿Qué significa 'Biblia'?", "opciones": ["Palabra", "Libros", "Sagrado", "Historia"], "respuesta_correcta": 1, "nivel": 4, "cita_biblica": "Etimología"},
    {"pregunta": "¿Quién fue el padre de Noé?", "opciones": ["Enoc", "Lamec", "Matusalén", "Jared"], "respuesta_correcta": 1, "nivel": 5, "cita_biblica": "Génesis 5:28"},
    {"pregunta": "¿En qué libro está la historia de Cornelio?", "opciones": ["Mateo", "Hechos", "Romanos", "Gálatas"], "respuesta_correcta": 1, "nivel": 6, "cita_biblica": "Hechos 10"},
    {"pregunta": "¿Cuántas veces vio Jesús a Pedro después de resucitar?", "opciones": ["No se especifica", "3", "2", "Varias"], "respuesta_correcta": 0, "nivel": 7, "cita_biblica": "Juan 21"},
    {"pregunta": "¿Quién fue el rey que no quitó los altares altos?", "opciones": ["David", "Salomón", "Ezequías", "Varios"], "respuesta_correcta": 3, "nivel": 8, "cita_biblica": "1 Reyes"},
    {"pregunta": "¿Qué mujer dejó su tierra por su suegra?", "opciones": ["Raquel", "Rut", "Ester", "Rebeca"], "respuesta_correcta": 1, "nivel": 9, "cita_biblica": "Rut 1"},
    {"pregunta": "¿Cuántas veces se menciona 'amor' en 1 Juan?", "opciones": ["5", "Más de 30", "10", "0"], "respuesta_correcta": 1, "nivel": 10, "cita_biblica": "1 Juan"},
    {"pregunta": "¿Quién fue el padre de Ismael?", "opciones": ["Abraham", "Isaac", "Jacob", "Lot"], "respuesta_correcta": 0, "nivel": 11, "cita_biblica": "Génesis 16:15"},
    {"pregunta": "¿En qué ciudad estaba el templo de Dios?", "opciones": ["Belén", "Jerusalén", "Nazaret", "Samaria"], "respuesta_correcta": 1, "nivel": 12, "cita_biblica": "1 Reyes 6"},
    {"pregunta": "¿Qué profeta fue llamado en su juventud?", "opciones": ["Isaías", "Jeremías", "Ezequiel", "Daniel"], "respuesta_correcta": 1, "nivel": 13, "cita_biblica": "Jeremías 1:6"},
    {"pregunta": "¿Cuántos años reinó David?", "opciones": ["30", "40", "33", "50"], "respuesta_correcta": 1, "nivel": 14, "cita_biblica": "1 Reyes 2:11"},
    {"pregunta": "¿Quién fue el rey que quemó incienso en el templo?", "opciones": ["Uzías", "Ezequías", "Manasés", "Varios"], "respuesta_correcta": 0, "nivel": 15, "cita_biblica": "2 Crónicas 26"},
    {"pregunta": "¿Qué fruto del Espíritu sigue al amor en Gálatas 5?", "opciones": ["Gozo", "Paz", "Paciencia", "Paz"], "respuesta_correcta": 0, "nivel": 1, "cita_biblica": "Gálatas 5:22"},
    {"pregunta": "¿Quién fue el profeta que vio huesos secos?", "opciones": ["Daniel", "Ezequiel", "Isaías", "Jeremías"], "respuesta_correcta": 1, "nivel": 2, "cita_biblica": "Ezequiel 37"},
    {"pregunta": "¿Cuántos hijos tuvo Lot?", "opciones": ["2 hijas", "Pocos", "No se detalla", "Varios"], "respuesta_correcta": 0, "nivel": 3, "cita_biblica": "Génesis 19"},
    {"pregunta": "¿En qué río Ezequiel tuvo visiones?", "opciones": ["Jordán", "Quebar", "Éufrates", "Nilo"], "respuesta_correcta": 1, "nivel": 4, "cita_biblica": "Ezequiel 1:1"},
    {"pregunta": "¿Quién fue el rey que buscó a David para matarlo?", "opciones": ["Absalón", "Saúl", "Ish-boset", "Joab"], "respuesta_correcta": 1, "nivel": 5, "cita_biblica": "1 Samuel 18"},
    {"pregunta": "¿Cuántas cartas escribió Juan?", "opciones": ["1", "2", "3", "4"], "respuesta_correcta": 3, "nivel": 7, "cita_biblica": "1, 2, 3 Juan + Apocalipsis"},
    {"pregunta": "¿Quién fue el padre de Moisés?", "opciones": ["Amram", "Aarón", "Leví", "Ceoré"], "respuesta_correcta": 0, "nivel": 8, "cita_biblica": "Éxodo 6:20"},
    {"pregunta": "¿En qué lugar Jesús dio el Sermón del Monte?", "opciones": ["Jerusalén", "Un monte en Galilea", "Jordán", "Nazaret"], "respuesta_correcta": 1, "nivel": 9, "cita_biblica": "Mateo 5:1"},
    {"pregunta": "¿Qué tribu no recibió tierra en Canaán?", "opciones": ["Leví", "Judá", "Benjamín", "Efraín"], "respuesta_correcta": 0, "nivel": 10, "cita_biblica": "Josué 13:33"},
    {"pregunta": "¿Quién fue el rey que tuvo 300 concubinas?", "opciones": ["David", "Salomón", "Roboam", "Acab"], "respuesta_correcta": 1, "nivel": 11, "cita_biblica": "1 Reyes 11:3"},
    {"pregunta": "¿Cuántos años tenía Josué cuando murió?", "opciones": ["100", "110", "120", "90"], "respuesta_correcta": 1, "nivel": 12, "cita_biblica": "Josué 24:29"},
    {"pregunta": "¿Qué significa 'Mesías'?", "opciones": ["Rey", "Ungido", "Salvador", "Profeta"], "respuesta_correcta": 1, "nivel": 13, "cita_biblica": "Griego/Hebreo"},
    {"pregunta": "¿Quién fue el profeta que profetizó el nacimiento de Juan?", "opciones": ["Isaías", "Gabriel", "Un ángel", "Malaquías"], "respuesta_correcta": 2, "nivel": 14, "cita_biblica": "Lucas 1:13"},
    {"pregunta": "¿En qué libro está 'No sólo de pan vivirá el hombre'?", "opciones": ["Éxodo", "Deuteronomio", "Levítico", "Números"], "respuesta_correcta": 1, "nivel": 15, "cita_biblica": "Deuteronomio 8:3"},
]

with open(RUTA, 'r', encoding='utf-8') as f:
    data = json.load(f)

antes = len(data['preguntas'])
data['preguntas'].extend(MAS)
despues = len(data['preguntas'])

with open(RUTA, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Se agregaron {len(MAS)} preguntas más. Total: {despues}")
