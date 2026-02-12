import 'dart:async';
import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:flutter/foundation.dart';
import '../config.dart';
import '../models/question.dart';

class GameService extends ChangeNotifier {
  List<Question> _preguntas = [];
  int _preguntaIndice = 0;
  Question? _preguntaActual;
  int _tiempoRestante = 30;
  Timer? _timer;
  bool _gameInProgress = false;
  bool _comodin5050 = false;
  bool _comodinPublico = false;
  bool _comodinBusqueda = false;
  bool _opcionesBloqueadas = false;

  List<Question> get preguntas => _preguntas;
  int get preguntaIndice => _preguntaIndice;
  Question? get preguntaActual => _preguntaActual;
  int get tiempoRestante => _tiempoRestante;
  bool get gameInProgress => _gameInProgress;
  bool get comodin5050 => _comodin5050;
  bool get comodinPublico => _comodinPublico;
  bool get comodinBusqueda => _comodinBusqueda;
  bool get opcionesBloqueadas => _opcionesBloqueadas;

  Future<void> loadQuestions() async {
    try {
      final json = await rootBundle.loadString('assets/preguntas/preguntas_biblicas.json');
      final data = jsonDecode(json) as Map<String, dynamic>;
      final list = (data['preguntas'] as List?)
          ?.map((e) => Question.fromJson(Map<String, dynamic>.from(e as Map)))
          .toList() ?? [];
      list.shuffle();
      _preguntas = list.take(15).toList();
    } catch (e) {
      if (kDebugMode) print('Error loading questions: $e');
      _preguntas = _defaultQuestions();
    }
    notifyListeners();
  }

  List<Question> _defaultQuestions() {
    return [
      Question(
        pregunta: '¿Cuántos días tardó Dios en crear el mundo?',
        opciones: ['3 días', '6 días', '7 días', '40 días'],
        respuestaCorrecta: 1,
        nivel: 1,
        citaBiblica: 'Génesis 1',
      ),
    ];
  }

  void startGame() {
    if (_preguntas.isEmpty) return;
    _preguntaIndice = 0;
    _comodin5050 = false;
    _comodinPublico = false;
    _comodinBusqueda = false;
    _opcionesBloqueadas = false;
    _gameInProgress = true;
    _loadCurrentQuestion();
    notifyListeners();
  }

  void _loadCurrentQuestion() {
    _timer?.cancel();
    if (_preguntaIndice >= _preguntas.length) {
      _endGame(winner: true);
      return;
    }
    _preguntaActual = _preguntas[_preguntaIndice];
    _tiempoRestante = 30;
    _opcionesBloqueadas = false;
    _timer = Timer.periodic(const Duration(seconds: 1), (_) => _tick());
    notifyListeners();
  }

  void _tick() {
    _tiempoRestante--;
    notifyListeners();
    if (_tiempoRestante <= 0) {
      _timer?.cancel();
      _opcionesBloqueadas = true;
      _endGame(winner: false);
    }
  }

  void answer(int index) {
    if (_opcionesBloqueadas || _preguntaActual == null) return;
    _timer?.cancel();
    _opcionesBloqueadas = true;
    final correct = index == _preguntaActual!.respuestaCorrecta;
    if (correct) {
      _preguntaIndice++;
      notifyListeners();
      Future.delayed(const Duration(milliseconds: 1800), () {
        _loadCurrentQuestion();
      });
    } else {
      _endGame(winner: false);
    }
    notifyListeners();
  }

  void _endGame({required bool winner}) {
    _gameInProgress = false;
    _timer?.cancel();
    notifyListeners();
  }

  void use5050() {
    if (_comodin5050 || _preguntaActual == null) return;
    _comodin5050 = true;
    notifyListeners();
  }

  void usePublico() {
    if (_comodinPublico || _preguntaActual == null) return;
    _comodinPublico = true;
    notifyListeners();
  }

  void useBusqueda() {
    if (_comodinBusqueda || _preguntaActual == null) return;
    _comodinBusqueda = true;
    notifyListeners();
  }

  List<int> get hiddenOptionIndices {
    if (!_comodin5050 || _preguntaActual == null) return [];
    final correct = _preguntaActual!.respuestaCorrecta;
    final wrong = [0, 1, 2, 3]..remove(correct);
    wrong.shuffle();
    return wrong.take(2).toList();
  }

  List<int> get publicoPercentages {
    if (_preguntaActual == null) return [0, 0, 0, 0];
    final correct = _preguntaActual!.respuestaCorrecta;
    final p = List<int>.filled(4, 0);
    p[correct] = 45 + (DateTime.now().millisecond % 26);
    int rest = 100 - p[correct];
    final others = [0, 1, 2, 3]..remove(correct);
    others.shuffle();
    for (final i in others) {
      if (rest <= 0) break;
      p[i] = rest > 20 ? 5 + (DateTime.now().millisecond % 15) : rest;
      rest -= p[i];
    }
    p[others.last] = (p[others.last] + rest).clamp(0, 100);
    return p;
  }

  /// Índice en [premios] del último nivel de seguridad alcanzado, o -1 si no llegó a ninguno.
  int get premioSeguridad {
    if (_preguntaIndice >= seguridad[1]) return seguridad[1] - 1;
    if (_preguntaIndice >= seguridad[0]) return seguridad[0] - 1;
    return -1;
  }

  void exitGame() {
    _gameInProgress = false;
    _timer?.cancel();
    notifyListeners();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}
