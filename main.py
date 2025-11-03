import pygame
from game_state_manager import GameStateManager

pygame.init()

resolution = (1920, 1080)
initial_ball_speed = 400
fps = 180

# Ventana
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
pygame.display.set_caption("Verong Pong")

# Manager de estados del juego
manager = GameStateManager(screen, resolution[0], resolution[1], initial_ball_speed)

clock = pygame.time.Clock()

# Bucle principal del juego
running = True
while running == True:
    # Limitar el delta_time para evitar bloqueos al arrastrar/redimensionar la ventana
    delta_time = clock.tick(fps) / 1000

    # Clampeamos para mantener la app reactiva durante y después del resize
    if delta_time > 0.25:
        # Considerar el frame como "resumido" de una pausa larga
        delta_time = 1.0 / 60.0
    else:
        delta_time = min(delta_time, 1.0 / 60.0)
        
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.handle_event(event)

    manager.update(delta_time)
    manager.draw()