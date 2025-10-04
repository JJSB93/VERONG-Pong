import pygame
#Declaro variables
(width, height) = (800, 600)
rectangulo = pygame.Rect(400, 300, 30, 50)
screen = pygame.display.set_mode((width, height))
#Inicializa pygame 
pygame.init()
pygame.display.set_caption("Juego de Vero")


#Bucle del juego
running = True
while running:
    #Captura de eventos
    events = pygame.event.get()
    #Asigancion del evento closeWindow
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit ()

    #Pinta un fondo nuevo
    screen.fill((0,0,0))

    pygame.draw.rect(screen, (255,255,255), rectangulo)
    
    #Actualiza la screen
    pygame.display.flip()
    
       
