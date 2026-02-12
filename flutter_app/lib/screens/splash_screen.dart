import 'dart:math';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config.dart';
import '../services/game_service.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  double _progress = 0;
  late String _versiculo;

  @override
  void initState() {
    super.initState();
    _versiculo = versiculosBiblicos[Random().nextInt(versiculosBiblicos.length)];
    _load();
  }

  Future<void> _load() async {
    final game = context.read<GameService>();
    await game.loadQuestions();
    if (!mounted) return;
    setState(() => _progress = 100);
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        if (_progress >= 100) {
          Navigator.of(context).pushReplacementNamed('/menu');
        }
      },
      child: Scaffold(
        backgroundColor: const Color(0xFF050508),
        body: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
            child: Column(
              children: [
                const SizedBox(height: 40),
                const Text(
                  'LOADING',
                  style: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF33CCFF),
                  ),
                ),
                const SizedBox(height: 12),
                const Text(
                  '¿QUIÉN QUIERE SER MILLONARIO? - BÍBLICO',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.white70,
                  ),
                ),
                const SizedBox(height: 32),
                LinearProgressIndicator(
                  value: _progress / 100,
                  backgroundColor: Colors.white24,
                  valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFF33CCFF)),
                ),
                const SizedBox(height: 16),
                Expanded(
                  child: Center(
                    child: Text(
                      _versiculo,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 15,
                        color: Colors.white,
                        height: 1.4,
                      ),
                    ),
                  ),
                ),
                const Text(
                  'Toca la pantalla para empezar cuando termine la carga',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 12, color: Colors.white54),
                ),
                const SizedBox(height: 24),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
