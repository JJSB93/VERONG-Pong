import pygame
#Declaro variables
(width, height) = (1000, 800)
pala1 = pygame.Rect(150, 300, 15, 60)
pala2 = pygame.Rect(850, 300, 15, 60)
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

    #Registrar teclas pulsadas
    keys_state = pygame.key.get_pressed()
    if keys_state[pygame.K_w]:
        pala1.y -= 1
    elif keys_state[pygame.K_s]:
        pala1.y += 1

    if keys_state[pygame.K_UP]:
        pala2.y -= 1
    elif keys_state[pygame.K_DOWN]:
        pala2.y += 1
    

    #Pinta un fondo nuevo
    screen.fill((0,0,0))

    pygame.draw.rect(screen, (255,255,255), pala1)
    pygame.draw.rect(screen, (255,255,255), pala2)

    #Actualiza la screen
    pygame.display.flip()


#Desinicializacion de pygame
pygame.quit()
