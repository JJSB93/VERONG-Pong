import pygame
from game_state_manager import GameStateManager


pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

pygame.display.set_caption("Verong Pong")

manager = GameStateManager(screen, 1920, 1080, 400)

clock = pygame.time.Clock()
running = True
while running == True:
    delta_time = clock.tick_busy_loop(140) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.handle_event(event)

    manager.update(delta_time)
    manager.draw()