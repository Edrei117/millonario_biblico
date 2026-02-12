import 'package:flutter/material.dart';
import '../config.dart';

class PrizeLadder extends StatelessWidget {
  final int currentLevel;

  const PrizeLadder({super.key, required this.currentLevel});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        return ListView.builder(
          shrinkWrap: true,
          physics: const BouncingScrollPhysics(),
          itemCount: 15,
          itemBuilder: (context, i) {
            final nivel = i + 1;
            final premio = nivel <= premios.length ? premios[nivel - 1] : r'$0';
            final isCurrent = nivel == currentLevel;
            final isPassed = nivel <= currentLevel - 1;
            final isSeguro = seguridad.contains(nivel);
            final text = nivel == 15 ? 'Premio' : premio;

            Color bgColor;
            Color textColor;
            if (isCurrent) {
              bgColor = const Color(0xFF333366);
              textColor = Colors.white;
            } else if (isPassed) {
              bgColor = const Color(0xFF1A1A33);
              textColor = Colors.white54;
            } else {
              bgColor = const Color(0xFF1A1A4D);
              textColor = Colors.white70;
            }

            return Padding(
              padding: const EdgeInsets.only(bottom: 2),
              child: Container(
                height: 26,
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: bgColor,
                  borderRadius: BorderRadius.circular(4),
                  boxShadow: isCurrent ? [const BoxShadow(color: Colors.white24, blurRadius: 2)] : null,
                ),
                child: Row(
                  children: [
                    if (isSeguro)
                      SizedBox(
                        width: 52,
                        child: Text(
                          nivel == 5 ? 'Seguro 1' : 'Seguro 2',
                          style: const TextStyle(
                            fontSize: 9,
                            color: Color(0xFFD6AE1F),
                          ),
                        ),
                      ),
                    SizedBox(
                      width: 24,
                      child: Text(
                        '$nivel',
                        style: TextStyle(
                          fontSize: 12,
                          color: textColor,
                          fontWeight: isCurrent ? FontWeight.bold : null,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                    Expanded(
                      child: Text(
                        text,
                        style: TextStyle(
                          fontSize: 11,
                          color: textColor,
                          fontWeight: isCurrent ? FontWeight.bold : null,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }
}
