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
    delta_time = clock.tick(fps) / 1000
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.handle_event(event)

    manager.update(delta_time)
    manager.draw()