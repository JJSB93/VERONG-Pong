import pygame

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

pygame.display.set_caption("Verong Pong")

clock = pygame.time.Clock()
running = True
while running == True:
    