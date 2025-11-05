# VERONG Pong

Un Pong realizado con Pygame con un pequeño framework de estados (Splash, Menú, Entrada de Nombres, Juego y Pausa), entrada de texto personalizada, y un sistema de colisiones continuo con correcciones de precisión.

## Características

- Estados del juego con ciclo de vida claro: `on_enter → layout → resize → handle_event → update → draw`.
- Un único `pygame.display.flip()` centralizado en el gestor, para evitar parpadeos y duplicados.
- Splash screen con fade-in/fade-out.
- Menú con botones (hover + atenuación suave) y detección de clic por borde (DOWN/UP).
- Entrada de texto con caret parpadeante, edición con flechas, Backspace/Delete y longitud máxima.
- Sistema de colisiones continuo con epsilon y corrección anti-atravesado.
- Recolocación de UI en `VIDEORESIZE` sin “salto” del primer frame (layout antes del primer draw).
- Clamp del `delta_time` para evitar bloqueos al redimensionar/arrastrar la ventana.

## Controles

- Menú: ratón para hacer clic; tecla J también inicia partida.
- NameInput: ratón para foco; teclado para escribir nombres; Enter continúa; Escape vuelve al menú.
- Juego: W/S mueven la pala izquierda, Flechas ↑/↓ la pala derecha. G realiza el saque si la bola está parada. Escape pausa.
- Pausa: ratón para los botones; Escape reanuda.

# VERONG Pong

Juego Pong en Python con Pygame, construido paso a paso a partir de una bitácora de desarrollo: desde el prototipo básico hasta una arquitectura por estados con UI, entrada de texto y colisiones robustas.

## Características

- Estados del juego con ciclo de vida claro: `on_enter → layout → resize → handle_event → update → draw`.
- Flip único por frame (centralizado) para evitar parpadeos y duplicados.
- Splash screen con fade-in/fade-out y texto con pulso de color.
- Menú con botones (hover + atenuación suave) y detección de clic por borde (DOWN/UP).
- Entrada de texto con caret parpadeante, edición con flechas, Backspace/Delete y longitud máxima.
- Colisiones continuas (tiempo-de-impacto) con `EPSILON` y corrección anti-atravesado.
- Recolocación de UI en `VIDEORESIZE` sin “salto” del primer frame (layout antes de dibujar).
- Clamp del `delta_time` para evitar bloqueos al redimensionar/arrastrar la ventana.

## Controles

- Menú: ratón para hacer clic; tecla J también inicia partida.
- Entrada de nombres: clic para foco; teclado para escribir; Enter continúa; Escape vuelve al menú.
- Juego: W/S mueven la pala izquierda; Flechas ↑/↓ la pala derecha; G saca si la bola está parada; Escape pausa.
- Pausa: ratón para botones; Escape reanuda.

## Requisitos e instalación

Requisitos: Python 3.9+ y `pygame`.

```bash
# (Opcional) Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS

# Instalar dependencias
pip install pygame

# Ejecutar
python main.py
```

## Arquitectura y ciclo de vida

- `GameStateManager` orquesta estados, eventos globales (incl. `VIDEORESIZE`) y realiza un único `pygame.display.flip()` por frame.
- Cada estado implementa:
  - `on_enter()`: prepara recursos y llama a `layout()` antes del primer `draw()`.
  - `layout()/resize()`: posiciona elementos según el tamaño de ventana.
  - `handle_event()/update()/draw()`: flujo principal de interacción, lógica y render.
- UI:
  - `Button`: hover + fade; clic por borde con `MOUSEBUTTONDOWN/UP`.
  - `TextInput`: foco por clic, caret con blink, edición básica (flechas, Backspace/Delete, longitud máxima).

## Estructura del repositorio

- `main.py`: bucle principal; limitación de FPS y clamp del `delta_time`.
- `game_state_manager.py`: gestor de estados y estados (`SplashState`, `MenuState`, `NameInputState`, `PlayingState`, `PausedState`).
- `game_data.py`: datos de la partida (marcador, bola, velocidad, etc.).
- `button.py`: botón con animación y detección de clic por borde.
- `text_input.py`: entrada de texto con caret y edición.
- `splash_state.py`: splash con fade y pulso de color.
- `documentation/`: documentación y notas técnicas.

## Cronología resumida (desde la bitácora)

1. Movimiento básico, colisiones y límite de FPS.
2. Marcador, reinicio de bola y centrado.
3. `GameData` para centralizar estado y `reset()` limpio.
4. Menú principal y pausa con botones.
5. Migración a `GameStateManager` y separación por estados.
6. Planificación de opciones (nombres, dificultad, IA).
7. Entrada de texto y estado `NameInputState` con foco y caret.
8. Splash screen con fade; flip único centralizado; layout antes del primer draw.
9. Robustez: clamp de `delta_time` en resize/arrastre; corrección anti-atravesado con `EPSILON`.

## Problemas y soluciones clave

- Congelación al redimensionar/arrastrar: clamp de `delta_time` para evitar picos de tiempo.
- “Salto” de layout al entrar en un estado: `on_enter()` llama a `layout()` antes del primer `draw()`.
- Splash negra o parpadeos: overlay con alpha actualizado y flip único en el gestor.
- Click residual que saltaba estados: botones con detección por borde basada en eventos.
- Bola atravesando palas: ventana de colisión `t <= remaining_time + EPSILON` + corrección final.

## Reconocimientos

Este proyecto se realizó por el autor con aprendizaje y guía de ChatGPT. Todas las decisiones, implementación final y validaciones se llevaron a cabo por el autor.

## Licencia

MIT. Ver `LICENSE`.
