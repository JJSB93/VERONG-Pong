import pygame, math

EPSILON = 1e-6
BALL_RADIUS = 10

#Funciones para detectar colision matematica
def collision_x(x, vx, r, pala_edge): # <-- Calcula el momento en el que ocurre la colision
    if vx > 0:
        t = (pala_edge - r - x) / vx
        return t
    elif vx < 0:
        t = (pala_edge + r - x) / vx
        return t
    elif vx == 0:
        return None

def collision_y_check(y, vy, pala_rect, r, t): # <-- Comprueba si en el momento "t", la pala colisiona con "y"
    top = pala_rect.top
    bottom = pala_rect.bottom
    y_in_collision = y + vy * t
    return  top - r <= y_in_collision <= bottom + r

def collision_detection(prev_ball_real, ball_vel, pala_rect, r): # <-- Comprueba si hay colision con la pala 
    x, y = prev_ball_real                                            # y devuelve el momento dentro del frame donde 
    vx, vy = ball_vel                                           # ocurre la colision "t"
    # La bola se mueve hacia la izquierda
    if vx < 0:
        t = collision_x(x, vx, r, pala_rect.right)
        if t > 0 and collision_y_check(y, vy, pala_rect, r, t):
            return t
    # La bola se mueve hacia la derecha    
    elif vx > 0:
        t = collision_x(x, vx, r, pala_rect.left)
        if t > 0 and collision_y_check(y, vy, pala_rect, r, t):
            return t

    return None

#Funcion para calcular la distancia entre la colision y el centro de la pala
def relative_collision_point(ball_y, pala_center_y, pala_height):
    relative_y = (ball_y - pala_center_y)
    normalized_y = relative_y / (pala_height / 2)
    return max(-1,min(normalized_y, 1))


#Declaro variables
width = 1200
height = 800
resolution = (width, height)
screen = pygame.display.set_mode(resolution)
pala1_x = width * 0.15
pala2_x = width - (width * 0.15)
pala1 = pygame.Rect(pala1_x, 300, 15, 60)
pala2 = pygame.Rect(pala2_x, 300, 15, 60)
ball_center = (width * 0.5, height * 0.5)
ball_real = list(ball_center)
ball_vel = [0, 0]
pala1_y_real = pala1.y
pala2_y_real = pala2.y
speed = 300
game_clock = pygame.time.Clock()
pala_center_y = pala1.center[1]
max_bounce_angle = 15
b_angle_rad = 0.0

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
        pala1_y_real -= speed * delta_time
    elif keys_state[pygame.K_s]:
        pala1_y_real += speed * delta_time

    if keys_state[pygame.K_UP]:
        pala2_y_real -= speed * delta_time
    elif keys_state[pygame.K_DOWN]:
        pala2_y_real += speed * delta_time

    #Limitar el movimiento de las palas a los bordes 
    if pala1_y_real < 0:
        pala1_y_real = 0
    if pala1_y_real > height - pala1.height:
        pala1_y_real = height - pala1.height

    if pala2_y_real < 0:
        pala2_y_real = 0
    if pala2_y_real > height - pala2.height:
        pala2_y_real = height - pala2.height

    #Actualizar la posicion de pala.y mediante una variable
    # para poder aumentar y disminuir en decimales
    pala1.y = int(pala1_y_real)
    pala2.y = int(pala2_y_real)

    #Movimiento de la bola
    prev_ball_real = ball_real[:]
    ball_real[0] += ball_vel[0] * delta_time
    ball_real[1] += ball_vel[1] * delta_time

    ball_center = tuple(ball_real)
    
    #Colisiones y rebote con los margenes
    if ball_real[1] - BALL_RADIUS <= 0:
        ball_real[1] = 0 + BALL_RADIUS
        ball_vel[1] = - ball_vel[1]

    if ball_real[1] + BALL_RADIUS >= height:
        ball_real[1] = height - BALL_RADIUS
        ball_vel[1] = - ball_vel[1]

    #Colision con Pala1
    t = collision_detection(prev_ball_real, ball_vel, pala1, BALL_RADIUS)
    if t is not None and EPSILON < t <= delta_time - EPSILON:
        #Posicionamiento de la bola cuando colisiona    
        ball_real[0] = prev_ball_real[0] + ball_vel[0] * t
        ball_real[1] = prev_ball_real[1] + ball_vel[1] * t
        
        #Ajuste de la velocidad y del angulo del rebote 
        coll_point_y = relative_collision_point(ball_real[1], pala1.centery, pala1.height)
        bounce_angle = coll_point_y * max_bounce_angle
        bounce_angle_rad = math.radians(bounce_angle)
        if (speed * 1.1) <= 700:
            speed *= 1.1 
        ball_vel[0] = speed * math.cos(bounce_angle_rad)
        ball_vel[1] = speed * math.sin(bounce_angle_rad)
        
        #Posicionamiento de la bola despues del rebote
        remianing_time = delta_time - t
        ball_real[0] += ball_vel[0] * remianing_time
        ball_real[1] += ball_vel[1] * remianing_time

    #Colision con pala2
    t = collision_detection(prev_ball_real, ball_vel, pala2, BALL_RADIUS)
    if t is not None and EPSILON < t <= delta_time - EPSILON:
        #Posicionamiento de la bola cuando colisiona
        ball_real[0] = prev_ball_real[0] + ball_vel[0] * t
        ball_real[1] = prev_ball_real[1] + ball_vel[1] * t

        #Ajuste de la velocidad y del angulo del rebote 
        coll_point_y = relative_collision_point(ball_real[1], pala2.centery, pala2.height)
        bounce_angle = coll_point_y * max_bounce_angle
        bounce_angle_rad = math.radians(bounce_angle) 
        if (speed * 1.1) <= 700:
            speed *= 1.1
        ball_vel[0] = - speed * math.cos(bounce_angle_rad)
        ball_vel[1] = speed * math.sin(bounce_angle_rad)
        
        #Posicionamiento de la bola despues del rebote
        remianing_time = delta_time - t
        ball_real[0] -= ball_vel[0] * remianing_time
        ball_real[1] -= ball_vel[1] * remianing_time

    

    screen.fill((0,0,0))

    #Dibuja las palas
    pygame.draw.rect(screen, (255,255,255), pala1)
    pygame.draw.rect(screen, (255,255,255), pala2)
    pygame.draw.circle(screen, (255,255,255), ball_center, BALL_RADIUS)

    #Actualiza la screen
    pygame.display.flip()

    


#Desinicializacion de pygame
pygame.quit()
