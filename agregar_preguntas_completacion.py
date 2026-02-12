import json
import os

"""
Script para agregar preguntas de COMPLETACIÓN basadas en versículos
de la Biblia (versión Reina-Valera) al archivo preguntas_biblicas.json.

Ejecuta este archivo una sola vez con:

    python agregar_preguntas_completacion.py
"""

RUTA = os.path.join(os.path.dirname(__file__), "preguntas", "preguntas_biblicas.json")

# NOTA:
# - Formato compatible con el resto del juego:
#   { "pregunta": str, "opciones": [str, str, str, str],
#     "respuesta_correcta": int, "nivel": int, "cita_biblica": str }
# - Usamos preguntas de "completación" donde falta una palabra o parte del versículo.

PREGUNTAS_COMPLETACION = [
    {
        "pregunta": "Completa el versículo: \"Porque de tal manera amó Dios al mundo, que ha dado a su ______ unigénito\"",
        "opciones": ["Ángel", "Hijo", "Profeta", "Siervo"],
        "respuesta_correcta": 1,
        "nivel": 1,
        "cita_biblica": "Juan 3:16 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Jehová es mi ______; nada me faltará\"",
        "opciones": ["Roca", "Rey", "Pastor", "Escudo"],
        "respuesta_correcta": 2,
        "nivel": 1,
        "cita_biblica": "Salmos 23:1 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Todo lo puedo en ______ que me fortalece\"",
        "opciones": ["Dios", "el Espíritu", "Cristo", "el Señor"],
        "respuesta_correcta": 2,
        "nivel": 1,
        "cita_biblica": "Filipenses 4:13 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Yo soy el camino, y la verdad, y la ______\"",
        "opciones": ["Luz", "Puerta", "Vida", "Paz"],
        "respuesta_correcta": 2,
        "nivel": 1,
        "cita_biblica": "Juan 14:6 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"En el principio creó Dios los ______ y la tierra\"",
        "opciones": ["astros", "mares", "cielos", "pueblos"],
        "respuesta_correcta": 2,
        "nivel": 1,
        "cita_biblica": "Génesis 1:1 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Lámpara es a mis pies tu ______, y lumbrera a mi camino\"",
        "opciones": ["luz", "ley", "palabra", "verdad"],
        "respuesta_correcta": 2,
        "nivel": 1,
        "cita_biblica": "Salmos 119:105 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Porque la paga del pecado es ______\"",
        "opciones": ["castigo", "separación", "muerte", "dolor"],
        "respuesta_correcta": 2,
        "nivel": 2,
        "cita_biblica": "Romanos 6:23 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Mas la dádiva de Dios es vida ______ en Cristo Jesús Señor nuestro\"",
        "opciones": ["abundante", "plena", "santa", "eterna"],
        "respuesta_correcta": 3,
        "nivel": 2,
        "cita_biblica": "Romanos 6:23 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"El Señor es mi ______ y mi salvación; ¿de quién temeré?\"",
        "opciones": ["roca", "escudo", "luz", "fortaleza"],
        "respuesta_correcta": 3,
        "nivel": 2,
        "cita_biblica": "Salmos 27:1 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Clama a mí, y yo te ______\"",
        "opciones": ["sanaré", "salvaré", "ayudaré", "responderé"],
        "respuesta_correcta": 3,
        "nivel": 2,
        "cita_biblica": "Jeremías 33:3 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Bienaventurados los ______ de corazón, porque ellos verán a Dios\"",
        "opciones": ["puros", "humildes", "mansos", "limpios"],
        "respuesta_correcta": 3,
        "nivel": 2,
        "cita_biblica": "Mateo 5:8 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Porque por gracia sois ______ por medio de la fe\"",
        "opciones": ["justos", "santos", "benditos", "salvos"],
        "respuesta_correcta": 3,
        "nivel": 2,
        "cita_biblica": "Efesios 2:8 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"El temor de Jehová es el principio de la ______\"",
        "opciones": ["ciencia", "justicia", "vida", "sabiduría"],
        "respuesta_correcta": 3,
        "nivel": 3,
        "cita_biblica": "Proverbios 1:7 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Buscad primeramente el reino de ______ y su justicia\"",
        "opciones": ["los cielos", "Cristo", "los cielos de Dios", "Dios"],
        "respuesta_correcta": 3,
        "nivel": 3,
        "cita_biblica": "Mateo 6:33 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Y conoceréis la verdad, y la verdad os hará ______\"",
        "opciones": ["fuertes", "sabios", "justos", "libres"],
        "respuesta_correcta": 3,
        "nivel": 3,
        "cita_biblica": "Juan 8:32 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"El Señor es mi pastor; nada me ______\"",
        "opciones": ["angustiará", "asustará", "dañará", "faltará"],
        "respuesta_correcta": 3,
        "nivel": 3,
        "cita_biblica": "Salmos 23:1 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Estad quietos, y conoced que yo soy ______\"",
        "opciones": ["Jehová", "el Señor", "Santo", "Dios"],
        "respuesta_correcta": 3,
        "nivel": 3,
        "cita_biblica": "Salmos 46:10 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Mas buscad primeramente el reino de Dios y su ______\"",
        "opciones": ["misericordia", "voluntad", "gracia", "justicia"],
        "respuesta_correcta": 3,
        "nivel": 3,
        "cita_biblica": "Mateo 6:33 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"No temas, porque yo estoy ______\"",
        "opciones": ["cerca", "a tu lado", "delante", "contigo"],
        "respuesta_correcta": 3,
        "nivel": 4,
        "cita_biblica": "Isaías 41:10 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Echando toda vuestra ansiedad sobre él, porque él tiene ______ de vosotros\"",
        "opciones": ["misericordia", "amor", "gracia", "cuidado"],
        "respuesta_correcta": 3,
        "nivel": 4,
        "cita_biblica": "1 Pedro 5:7 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Bienaventurados los que lloran, porque ellos recibirán ______\"",
        "opciones": ["gozo", "paz", "esperanza", "consolación"],
        "respuesta_correcta": 3,
        "nivel": 4,
        "cita_biblica": "Mateo 5:4 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"El ladrón no viene sino para hurtar y matar y ______\"",
        "opciones": ["confundir", "engañar", "oprimir", "destruir"],
        "respuesta_correcta": 3,
        "nivel": 4,
        "cita_biblica": "Juan 10:10 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"De tal manera amó Dios al mundo, que ha dado a su Hijo ______\"",
        "opciones": ["amado", "santo", "perfecto", "unigénito"],
        "respuesta_correcta": 3,
        "nivel": 4,
        "cita_biblica": "Juan 3:16 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Pero los que esperan a Jehová tendrán nuevas ______\"",
        "opciones": ["misericordias", "victorias", "bendiciones", "fuerzas"],
        "respuesta_correcta": 3,
        "nivel": 4,
        "cita_biblica": "Isaías 40:31 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"De la abundancia del corazón habla la ______\"",
        "opciones": ["lengua", "mente", "persona", "boca"],
        "respuesta_correcta": 3,
        "nivel": 5,
        "cita_biblica": "Mateo 12:34 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"El justo por la fe ______\"",
        "opciones": ["andará", "triunfará", "vencerá", "vivirá"],
        "respuesta_correcta": 3,
        "nivel": 5,
        "cita_biblica": "Romanos 1:17 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Sed santos, porque yo soy ______\"",
        "opciones": ["justo", "bueno", "perfecto", "santo"],
        "respuesta_correcta": 3,
        "nivel": 5,
        "cita_biblica": "1 Pedro 1:16 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Honra a tu padre y a tu ______\"",
        "opciones": ["familia", "hermano", "prójimo", "madre"],
        "respuesta_correcta": 3,
        "nivel": 5,
        "cita_biblica": "Éxodo 20:12 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"No te dejaré, ni te ______\"",
        "opciones": ["olvidaré", "abandonaré", "apartaré", "desampararé"],
        "respuesta_correcta": 3,
        "nivel": 5,
        "cita_biblica": "Hebreos 13:5 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Amarás a tu prójimo como a ______\"",
        "opciones": ["tu hermano", "tu familia", "tu amigo", "ti mismo"],
        "respuesta_correcta": 3,
        "nivel": 5,
        "cita_biblica": "Mateo 22:39 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Sea vuestra palabra siempre con ______, sazonada con sal\"",
        "opciones": ["verdad", "amor", "sabiduría", "gracia"],
        "respuesta_correcta": 3,
        "nivel": 6,
        "cita_biblica": "Colosenses 4:6 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Porque no nos ha dado Dios espíritu de cobardía, sino de poder, de amor y de ______\"",
        "opciones": ["sabiduría", "fe", "paciencia", "dominio propio"],
        "respuesta_correcta": 3,
        "nivel": 6,
        "cita_biblica": "2 Timoteo 1:7 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Bienaventurados los pacificadores, porque ellos serán llamados ______ de Dios\"",
        "opciones": ["siervos", "amigos", "pueblo", "hijos"],
        "respuesta_correcta": 3,
        "nivel": 6,
        "cita_biblica": "Mateo 5:9 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Si Dios es por nosotros, ¿quién contra ______?\"",
        "opciones": ["su pueblo", "sus hijos", "la iglesia", "nosotros"],
        "respuesta_correcta": 3,
        "nivel": 6,
        "cita_biblica": "Romanos 8:31 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Porque donde esté vuestro tesoro, allí estará también vuestro ______\"",
        "opciones": ["pensamiento", "alma", "camino", "corazón"],
        "respuesta_correcta": 3,
        "nivel": 6,
        "cita_biblica": "Mateo 6:21 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Pedid, y se os ______; buscad, y hallaréis\"",
        "opciones": ["abrirá", "multiplicará", "responderá", "dará"],
        "respuesta_correcta": 3,
        "nivel": 6,
        "cita_biblica": "Mateo 7:7 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"De modo que si alguno está en Cristo, nueva ______ es\"",
        "opciones": ["vida", "persona", "creación", "criatura"],
        "respuesta_correcta": 3,
        "nivel": 7,
        "cita_biblica": "2 Corintios 5:17 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Porque el Hijo del Hombre vino a buscar y a ______ lo que se había perdido\"",
        "opciones": ["restaurar", "sanar", "levantar", "salvar"],
        "respuesta_correcta": 3,
        "nivel": 7,
        "cita_biblica": "Lucas 19:10 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Y el Verbo se hizo ______, y habitó entre nosotros\"",
        "opciones": ["hombre", "luz", "siervo", "carne"],
        "respuesta_correcta": 3,
        "nivel": 7,
        "cita_biblica": "Juan 1:14 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Velad y ______, para que no entréis en tentación\"",
        "opciones": ["ayunad", "confesad", "creed", "orad"],
        "respuesta_correcta": 3,
        "nivel": 7,
        "cita_biblica": "Mateo 26:41 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Y recibiréis poder, cuando haya venido sobre vosotros el ______ Santo\"",
        "opciones": ["Fuego", "Señor", "ángel", "Espíritu"],
        "respuesta_correcta": 3,
        "nivel": 7,
        "cita_biblica": "Hechos 1:8 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Haya, pues, en vosotros este sentir que hubo también en ______\"",
        "opciones": ["el Señor", "Dios", "el Hijo", "Cristo Jesús"],
        "respuesta_correcta": 3,
        "nivel": 7,
        "cita_biblica": "Filipenses 2:5 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Mas el fruto del Espíritu es amor, gozo, ______, paciencia...\"",
        "opciones": ["fe", "bondad", "templanza", "paz"],
        "respuesta_correcta": 3,
        "nivel": 8,
        "cita_biblica": "Gálatas 5:22 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"No os conforméis a este siglo, sino transformaos por medio de la renovación de vuestro ______\"",
        "opciones": ["espíritu", "corazón", "pensamiento", "entendimiento"],
        "respuesta_correcta": 3,
        "nivel": 8,
        "cita_biblica": "Romanos 12:2 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"El que habita al abrigo del Altísimo morará bajo la sombra del ______\"",
        "opciones": ["Santo", "Eterno", "Altísimo", "Omnipotente"],
        "respuesta_correcta": 3,
        "nivel": 8,
        "cita_biblica": "Salmos 91:1 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"Mejor es obedecer que ______\"",
        "opciones": ["prometer", "ofrendar", "enseñar", "sacrificar"],
        "respuesta_correcta": 3,
        "nivel": 8,
        "cita_biblica": "1 Samuel 15:22 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"En el mundo tendréis aflicción; pero confiad, yo he ______ al mundo\"",
        "opciones": ["juzgado", "cambiado", "salvado", "vencido"],
        "respuesta_correcta": 3,
        "nivel": 8,
        "cita_biblica": "Juan 16:33 (Reina-Valera)"
    },
    {
        "pregunta": "Completa: \"El cielo y la tierra pasarán, pero mis ______ no pasarán\"",
        "opciones": ["mandamientos", "obras", "leyes", "palabras"],
        "respuesta_correcta": 3,
        "nivel": 8,
        "cita_biblica": "Mateo 24:35 (Reina-Valera)"
    },
]


def main() -> None:
    with open(RUTA, "r", encoding="utf-8") as f:
        data = json.load(f)

    antes = len(data.get("preguntas", []))
    data["preguntas"].extend(PREGUNTAS_COMPLETACION)
    despues = len(data["preguntas"])

    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Se agregaron {len(PREGUNTAS_COMPLETACION)} preguntas de completación con opciones mezcladas. Total: {despues}")


if __name__ == "__main__":
    main()

