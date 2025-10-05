import pygame
#Funciones para detectar colision matematica
def collision_x(x, vx, r, pala_edge): # <-- Calcula el momento en el que ocurre la colision
    if vx > 0:
        t = (pala_edge - r - x) / vx
        return t
    elif vx < 0:
        t = (pala_edge + r - x) / vx
        return t

def collision_y_check(y, vy, pala_rect, r, t): # <-- Comprueba si en el momento "t", la pala colisiona con "y"
    top = pala_rect.top
    bottom = pala_rect.bottom
    y_in_collision = y + vy * t
    return  top - r <= y_in_collision <= bottom + r

def collision_detection(ball_real, ball_vel, pala_x, r): # <-- Comprueba si hay colision con la pala 
    x, y = ball_real                                            # y devuelve el momento dentro del frame donde 
    vx, vy = ball_vel                                           # ocurre la colision "t"
    # La bola se mueve hacia la izquierda
    if vx < 0:
        t = collision_x(x, vx, r, pala_x.right)
        if 0 < t < 1 and collision_y_check(y, vy, pala_x, r, t):
            return t
    # La bola se mueve hacia la derecha    
    elif vx > 0:
        t = collision_x(x, vx, r, pala_x.left)
        if 0 < t < 1 and collision_y_check(y, vy, pala_x, r, t):
            return t

    return None


#Declaro variables
(width, height) = (1000, 800)
screen = pygame.display.set_mode((width, height))
pala1 = pygame.Rect(150, 300, 15, 60)
pala2 = pygame.Rect(850, 300, 15, 60)
ball_center = (500, 400)
ball_real = list(ball_center)
BALL_RADIUS = 10
ball_vel = [0, 0]
pala1_y_real = pala1.y
pala2_y_real = pala2.y
velocidad = 300
game_clock = pygame.time.Clock()


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

    #Comenzar movimiento de la bola
    if ball_vel[0] == 0:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    ball_vel[0] = 200

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
    prev_ball_real = ball_real[:]
    ball_real[0] += ball_vel[0] * delta_time
    ball_real[1] += ball_vel[1] * delta_time

    ball_center = tuple(ball_real)
    
    #Colisiones
    ball_coll_box = pygame.Rect(0, 0, (2 * BALL_RADIUS), (2 * BALL_RADIUS))
    ball_coll_box.center = ball_center

    if ball_coll_box.colliderect(pala1) or (ball_coll_box.left <= pala1.right):
        ball_real[0] = pala1.right + BALL_RADIUS
        ball_vel[0] = -1.2 * ball_vel[0]

    elif ball_coll_box.colliderect(pala2) or (ball_coll_box.right >= pala2.left):
        ball_real[0] = pala2.left - BALL_RADIUS
        ball_vel[0] = -1.2 * ball_vel[0]
    
    

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
