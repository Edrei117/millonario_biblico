import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'services/game_service.dart';
import 'screens/splash_screen.dart';
import 'screens/menu_screen.dart';
import 'screens/game_screen.dart';

void main() {
  runApp(const MillonarioApp());
}

class MillonarioApp extends StatelessWidget {
  const MillonarioApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => GameService(),
      child: MaterialApp(
        title: '¿Quién Quiere Ser Millonario? Bíblico',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          brightness: Brightness.dark,
          primaryColor: const Color(0xFFD6AE1F),
          colorScheme: ColorScheme.dark(
            primary: const Color(0xFFD6AE1F),
            surface: const Color(0xFF0D0D1A),
            onSurface: Colors.white,
          ),
          useMaterial3: true,
        ),
        initialRoute: '/',
        routes: {
          '/': (context) => const SplashScreen(),
          '/menu': (context) => const MenuScreen(),
          '/game': (context) => const GameScreen(),
        },
      ),
    );
  }
}
