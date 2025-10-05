import pygame
#Declaro variables
(width, height) = (1000, 800)
screen = pygame.display.set_mode((width, height))
pala1 = pygame.Rect(150, 300, 15, 60)
pala2 = pygame.Rect(850, 300, 15, 60)
ball_center = (500, 400)
ball_real = list(ball_center)
BALL_RADIUS = 10
vel_x = 0
vel_y = 0
pala1_y_real = pala1.y
pala2_y_real = pala2.y
velocidad = 300
game_clock = pygame.time.Clock()
#ball_coll_box = pygame.Rect(ball_real[0], ball_real[1], 2 * BALL_RADIUS, 2 * BALL_RADIUS)

#Inicializa pygame 
pygame.init()
pygame.display.set_caption("Juego de Vero")


#Bucle del juego
running = True
while running:
    #Ajustar los fps
    delta_time = game_clock.tick(120) / 1000

    #Captura de eventos
    events = pygame.event.get()
    #Asigancion del evento closeWindow
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit ()

    #Registrar teclas pulsadas y mover las palas
    keys_state = pygame.key.get_pressed()

    if keys_state[pygame.K_w]:
        pala1_y_real -= velocidad * delta_time
    elif keys_state[pygame.K_s]:
        pala1_y_real += velocidad * delta_time

    if keys_state[pygame.K_UP]:
        pala2_y_real -= velocidad * delta_time
    elif keys_state[pygame.K_DOWN]:
        pala2_y_real += velocidad * delta_time
    #Limitar el movimiento de las palas a los bordes 
    if pala1_y_real < 0:
        pala1_y_real = 0
    if pala1_y_real > height - pala1.height:
        pala1_y_real = height - pala1.height

    if pala2_y_real < 0:
        pala2_y_real = 0
    if pala2_y_real > height - pala2.height:
        pala2_y_real = height - pala2.height
    #Actualizar la posicion de y mediante una variable
    # para poder aumentar y disminuir en decimales
    pala1.y = int(pala1_y_real)
    pala2.y = int(pala2_y_real)

    #Movimiento de la bola
    ball_real[0] += vel_x
    ball_real[1] += vel_y
    ball_center = tuple(ball_real)
    
    
    #Colisiones
    ball_coll_box = pygame.Rect(0, 0, (2 * BALL_RADIUS), (2 * BALL_RADIUS))
    ball_coll_box.center = ball_center

    if ball_coll_box.colliderect(pala2) or (ball_coll_box.x >= pala2.x): 
        vel_x -= 2.3 * vel_x
    elif ball_coll_box.colliderect(pala1) or (ball_coll_box.x + (2 * BALL_RADIUS) <= pala1.x):
        vel_x -= 2.3 * vel_x

    #Comenzar movimiento de la bola
    if vel_x == 0:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    vel_x = 1

    #Pinta un fondo nuevo
    screen.fill((0,0,0))

    #Dibuja las palas
    pygame.draw.rect(screen, (255,255,255), pala1)
    pygame.draw.rect(screen, (255,255,255), pala2)
    pygame.draw.circle(screen, (255,255,255), ball_center, BALL_RADIUS)

    #Actualiza la screen
    pygame.display.flip()

    


#Desinicializacion de pygame
pygame.quit()
