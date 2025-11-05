# VERONG Pong

Un Pong realizado con Pygame con un pequeño framework de estados (Splash, Menú, Entrada de Nombres, Juego y Pausa), entrada de texto personalizada, y un sistema de colisiones continuo con correcciones de precisión.

## Características

- Estados del juego con ciclo de vida claro: `on_enter → layout → resize → handle_event → update → draw`.
- Flip único por frame centralizado para evitar parpadeos y duplicados.
- Splash screen con fade-in/fade-out.
- Menú con botones (hover + atenuación suave) y detección de clic por borde (DOWN/UP).
- Entrada de texto con caret parpadeante, edición con flechas, Backspace/Delete y longitud máxima.
- Colisiones continuas (tiempo de impacto) con `EPSILON` y corrección anti-atravesado.
- Recolocación de UI en `VIDEORESIZE` sin “salto” del primer frame (layout antes del primer draw).
- Clamp del `delta_time` para evitar bloqueos al redimensionar/arrastrar la ventana.

## Controles

- Menú: ratón; (si está habilitado) tecla J para iniciar.
- Entrada de nombres: clic para foco; teclado para escribir; Enter continúa; Escape vuelve al menú.
- Juego: W/S (izquierda) · Flechas ↑/↓ (derecha) · G saca si la bola está parada · Escape pausa.
- Pausa: ratón para botones; Escape reanuda.

## Requisitos e instalación

Requisitos: Python 3.9+ y `pygame`.

```bash
# (Opcional) Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS (zsh)

# Instalar dependencias
pip install pygame

# Ejecutar
python main.py
```

## Arquitectura y ciclo de vida

- `GameStateManager` orquesta estados, `VIDEORESIZE` y realiza un único `pygame.display.flip()` por frame.
- Cada estado:
  - `on_enter()`: prepara y llama a `layout()` antes del primer `draw()`.
  - `layout()/resize()`: posicionamiento responsivo.
  - `handle_event()/update()/draw()`: interacción, lógica y render.
- UI:
  - `Button`: hover + fade; clic por borde con `MOUSEBUTTONDOWN/UP`.
  - `TextInput`: foco por clic, caret con blink y edición básica.

## Visuales y paleta

- Paleta Nocturna con acento menta:
  - Fondo: (10, 12, 18)
  - Elementos principales (bola/palas/textos claros): off‑white (242, 242, 242)
  - Línea central: gris claro (210, 210, 210)
  - Acento: menta (46, 230, 166) en bordes del marcador, hovers y detalles
- Palas con esquinas redondeadas y sombra sutil.
- Marcador con “pastilla” blanca y borde menta.
- Línea central discontinua en gris claro para no competir con la jugabilidad.

## Estructura del repositorio

- `main.py`: bucle principal; FPS y clamp de `delta_time`.
- `game_state_manager.py`: gestor y estados (`SplashState`, `MenuState`, `NameInputState`, `PlayingState`, `PausedState`).
- `game_data.py`: datos compartidos (puntuación, bola, velocidad, etc.).
- `button.py`: botón con animación y clic por borde.
- `text_input.py`: entrada de texto con caret y edición.
- `splash_state.py`: splash con fade.
- `documentation/`: documentación y notas técnicas.

## Cronología resumida (desde la bitácora)

1. Movimiento básico, colisiones y FPS.
2. Marcador y reinicio de bola.
3. `GameData` y `reset()` limpio.
4. Menú y pausa con botones.
5. `GameStateManager` y separación por estados.
6. Entrada de nombres (`TextInput`).
7. Splash con fade y flip único centralizado; layout antes del primer draw.
8. Robustez: clamp de `delta_time` y corrección anti‑atravesado con `EPSILON`.
9. Pulido visual y paleta unificada.

## Problemas y soluciones clave

- Congelación al redimensionar/arrastrar: clamp de `delta_time` para descartar picos.
- “Salto” al entrar en estado: `on_enter()` llama a `layout()` antes del primer `draw()`.
- Pantallas negras/parpadeos: overlay con alpha y flip único centralizado.
- Clic residual que saltaba estados: detección por borde (DOWN/UP) en botones.
- Bola atravesando palas: `t <= remaining_time + EPSILON` + corrección final.

## Reconocimientos

Proyecto realizado por el autor con aprendizaje y guía de ChatGPT. Las decisiones finales, la integración de código y las validaciones corrieron a cargo del autor.

## Licencia

MIT. Ver `LICENSE`.
