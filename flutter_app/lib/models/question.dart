class Question {
  final String pregunta;
  final List<String> opciones;
  final int respuestaCorrecta;
  final int nivel;
  final String? citaBiblica;

  Question({
    required this.pregunta,
    required this.opciones,
    required this.respuestaCorrecta,
    required this.nivel,
    this.citaBiblica,
  });

  factory Question.fromJson(Map<String, dynamic> json) {
    return Question(
      pregunta: json['pregunta'] as String? ?? '',
      opciones: List<String>.from(json['opciones'] as List? ?? []),
      respuestaCorrecta: (json['respuesta_correcta'] as num?)?.toInt() ?? 0,
      nivel: (json['nivel'] as num?)?.toInt() ?? 1,
      citaBiblica: json['cita_biblica'] as String?,
    );
  }
}
