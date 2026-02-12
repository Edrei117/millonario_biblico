import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config.dart';
import '../services/game_service.dart';
import '../widgets/prize_ladder.dart';

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  bool _endDialogShown = false;

  @override
  Widget build(BuildContext context) {
    return Consumer<GameService>(
      builder: (context, game, _) {
        if (!game.gameInProgress && game.preguntaIndice == 0 && game.preguntas.isNotEmpty) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            if (context.mounted) Navigator.of(context).pushReplacementNamed('/menu');
          });
          return const Scaffold(body: Center(child: CircularProgressIndicator()));
        }
        if (!game.gameInProgress && game.preguntaActual != null && !_endDialogShown) {
          _endDialogShown = true;
          WidgetsBinding.instance.addPostFrameCallback((_) {
            if (context.mounted) _showEndDialog(context, game);
          });
          return const Scaffold(body: Center(child: CircularProgressIndicator()));
        }
        return Scaffold(
          backgroundColor: const Color(0xFF0D0D1A),
          body: SafeArea(
            child: Stack(
              children: [
                // Fondo
                CustomScrollView(
                  slivers: [
                    SliverToBoxAdapter(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          _buildTopBar(context, game),
                          const SizedBox(height: 8),
                          const Text(
                            'QUIEN QUIERE SER',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          const SizedBox(height: 4),
                          _buildTimerCircle(context, game),
                          const Text(
                            'MILLONARIO',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          const SizedBox(height: 16),
                          _buildQuestionCard(game),
                          const SizedBox(height: 12),
                          _buildOptions(context, game),
                          const SizedBox(height: 80),
                        ],
                      ),
                    ),
                  ],
                ),
                // Escalera de premios a la derecha
                Positioned(
                  right: 0,
                  top: 0,
                  bottom: 0,
                  child: Container(
                    width: MediaQuery.of(context).size.width * 0.24,
                    margin: const EdgeInsets.only(top: 56, bottom: 16, right: 8),
                    decoration: BoxDecoration(
                      color: Colors.black26,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: PrizeLadder(currentLevel: game.preguntaIndice + 1),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildTopBar(BuildContext context, GameService game) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      child: Row(
        children: [
          _comodinChip(context, '50/50', game.comodin5050, () => game.use5050()),
          const SizedBox(width: 6),
          _comodinChip(context, 'Público', game.comodinPublico, () {
            game.usePublico();
            _showPublicoDialog(context, game);
          }),
          const SizedBox(width: 6),
          _comodinChip(context, 'Biblia', game.comodinBusqueda, () {
            game.useBusqueda();
            _showBusquedaDialog(context, game);
          }),
          const Spacer(),
          TextButton(
            onPressed: () {
              game.exitGame();
              Navigator.of(context).pushReplacementNamed('/menu');
            },
            child: const Text('SALIR', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
          ),
          const SizedBox(width: 8),
          CircleAvatar(
            radius: 20,
            backgroundColor: const Color(0xFF333366),
            child: Text(
              '${game.preguntaIndice + 1}',
              style: const TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _comodinChip(BuildContext context, String label, bool used, VoidCallback onTap) {
    return Material(
      color: used ? Colors.grey.shade800 : const Color(0xFF1E1E3D),
      borderRadius: BorderRadius.circular(20),
      child: InkWell(
        onTap: used ? null : onTap,
        borderRadius: BorderRadius.circular(20),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          child: Text(
            label,
            style: TextStyle(
              color: used ? Colors.grey : Colors.white,
              fontSize: 12,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTimerCircle(BuildContext context, GameService game) {
    final sec = game.tiempoRestante;
    return Container(
      width: 72,
      height: 72,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: const Color(0xFF1A1A33),
        border: Border.all(color: const Color(0xFF8066AA), width: 2),
      ),
      child: Center(
        child: Text(
          '$sec',
          style: TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.bold,
            color: sec <= 10 ? const Color(0xFFFF3333) : Colors.white,
          ),
        ),
      ),
    );
  }

  Widget _buildQuestionCard(GameService game) {
    final q = game.preguntaActual;
    if (q == null) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        decoration: BoxDecoration(
          color: const Color(0xFF1A1A33),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.white24),
        ),
        child: Text(
          q.pregunta,
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontSize: 16,
            color: Colors.white,
            fontWeight: FontWeight.w500,
            height: 1.3,
          ),
        ),
      ),
    );
  }

  Widget _buildOptions(BuildContext context, GameService game) {
    final q = game.preguntaActual;
    if (q == null) return const SizedBox.shrink();
    final hidden = game.hiddenOptionIndices;
    const letters = ['A', 'B', 'C', 'D'];

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        children: [
          Row(
            children: [
              Expanded(child: _optionButton(context, game, 0, letters[0], q.opciones[0], hidden.contains(0))),
              const SizedBox(width: 10),
              Expanded(child: _optionButton(context, game, 1, letters[1], q.opciones[1], hidden.contains(1))),
            ],
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Expanded(child: _optionButton(context, game, 2, letters[2], q.opciones[2], hidden.contains(2))),
              const SizedBox(width: 10),
              Expanded(child: _optionButton(context, game, 3, letters[3], q.opciones[3], hidden.contains(3))),
            ],
          ),
        ],
      ),
    );
  }

  Widget _optionButton(BuildContext context, GameService game, int index, String letter, String text, bool hidden) {
    if (hidden) {
      return const SizedBox(height: 56);
    }
    final disabled = game.opcionesBloqueadas;
    return Material(
      color: const Color(0xFF1A1A33),
      borderRadius: BorderRadius.circular(12),
      child: InkWell(
        onTap: disabled ? null : () => game.answer(index),
        borderRadius: BorderRadius.circular(12),
        child: Container(
          height: 56,
          padding: const EdgeInsets.symmetric(horizontal: 12),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.white24),
          ),
          child: Row(
            children: [
              Text(
                '◆ $letter',
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  text,
                  style: const TextStyle(color: Colors.white, fontSize: 14),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showPublicoDialog(BuildContext context, GameService game) {
    final p = game.publicoPercentages;
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2E),
        title: const Text('Consulta al público', style: TextStyle(color: Colors.white)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: ['A', 'B', 'C', 'D'].asMap().entries.map((e) {
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Row(
                children: [
                  Text('${e.value}:', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  const SizedBox(width: 8),
                  Expanded(
                    child: LinearProgressIndicator(
                      value: p[e.key] / 100,
                      backgroundColor: Colors.white24,
                      valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFF33CCFF)),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text('${p[e.key]}%', style: const TextStyle(color: Colors.white)),
                ],
              ),
            );
          }).toList(),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Entendido'),
          ),
        ],
      ),
    );
  }

  void _showBusquedaDialog(BuildContext context, GameService game) {
    final q = game.preguntaActual;
    final cita = q?.citaBiblica ?? 'Consulta tu Biblia para esta pregunta.';
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2E),
        title: const Text('Búsqueda bíblica', style: TextStyle(color: Colors.white)),
        content: Text(cita, style: const TextStyle(color: Colors.white70, height: 1.5)),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Entendido'),
          ),
        ],
      ),
    );
  }

  void _showEndDialog(BuildContext context, GameService game) {
    final winner = game.preguntaIndice >= 15;
    final idx = game.premioSeguridad;
    final premioFinal = winner ? premios[14] : (idx >= 0 ? premios[idx] : r'$0');
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2E),
        title: Text(
          winner ? '¡FELICIDADES!' : 'Fin del juego',
          style: TextStyle(color: winner ? const Color(0xFFD6AE1F) : Colors.white),
        ),
        content: Text(
          winner
              ? '¡ERES MILLONARIO!\n\nPremio: $premioFinal'
              : 'Ganaste: $premioFinal',
          style: const TextStyle(color: Colors.white70, height: 1.5),
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              Navigator.of(context).pushReplacementNamed('/menu');
            },
            child: const Text('Menú'),
          ),
          FilledButton(
            onPressed: () {
              Navigator.of(context).pop();
              game.startGame();
            },
            child: const Text('Nuevo juego'),
          ),
        ],
      ),
    );
  }
}
