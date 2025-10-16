import pygame, math

EPSILON = 1e-9
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

#Funcion para el calculo del momento de colision "t" con los bordes
def margins_collision(y, vy, r, height):
    if vy > 0:
        t = (height - r - y) / vy
        return t
    elif vy < 0:
        t = (r - y) / vy
        return t
    elif vy == 0:
        return None

#Declaro variables
width = 1900
height = 1080
resolution = (width, height)
screen = pygame.display.set_mode(resolution)
pala_height = 100
pala1_x = width * 0.15
pala2_x = width - (width * 0.15)
pala1_y = (height * 0.5) - (pala_height / 2)
pala2_y = (height * 0.5) - (pala_height / 2)
pala1 = pygame.Rect(pala1_x, pala1_y, 20, pala_height)
pala2 = pygame.Rect(pala2_x, pala2_y, 20, pala_height)
ball_center = (width * 0.5, height * 0.5)
ball_real = list(ball_center)
ball_render = ball_real[:]
ball_vel = [0, 0]
pala1_y_real = pala1.y
pala2_y_real = pala2.y
ball_speed = 400
ball_reset_speed = ball_speed
paddle_speed = 350
game_clock = pygame.time.Clock()
pala_center_y = pala1.center[1]
max_bounce_angle = 45
b_angle_rad = 0.0
t_min = None
p1_score = 0
p2_score = 0
service = False
 
p1_name = "Vero"
p2_name = "Juan"



#Inicializa pygame 
pygame.init()
pygame.display.set_caption("Juego de Vero")

#Inicializacion de la fuente 
font = pygame.font.SysFont("Arial", 38)

#Bucle del juego
running = True
while running:
    #Ajustar los fps
    delta_time = game_clock.tick(140) / 1000

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
                    if service:
                        ball_vel[0] = ball_reset_speed
                    else:
                        ball_vel[0] = -ball_reset_speed

    #Registrar teclas pulsadas y mover las palas
    keys_state = pygame.key.get_pressed()

    if keys_state[pygame.K_w]:
        pala1_y_real -= paddle_speed * delta_time
    elif keys_state[pygame.K_s]:
        pala1_y_real += paddle_speed * delta_time

    if keys_state[pygame.K_UP]:
        pala2_y_real -= paddle_speed * delta_time
    elif keys_state[pygame.K_DOWN]:
        pala2_y_real += paddle_speed * delta_time

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

    #Loop de resolucion de colisiones por sub-intervalos dentro del frame
    remaining_time = delta_time
    position = ball_real[:]
    while remaining_time > EPSILON:

        #Calcular los timepos de colision
        collision_times = []
        collision_times_filtered = []
        t_min = None
        t_pala1 = collision_detection(position, ball_vel, pala1, BALL_RADIUS)
        t_pala2 = collision_detection(position, ball_vel, pala2, BALL_RADIUS)
        t_margin = margins_collision(position[1], ball_vel[1], BALL_RADIUS, height)

        #Calcular la colision mas proxima en el tiempo
        collision_times = [("t_pala1", t_pala1), ("t_pala2", t_pala2), ("t_margin", t_margin)]
        
        for collision in collision_times:
            if collision[1] is not None and EPSILON < collision[1] <= (remaining_time - EPSILON):
                collision_times_filtered.append(collision)
        
        for collision in collision_times_filtered:
            if t_min == None or collision[1] < t_min[1]:
                t_min = collision

        if t_min == None:
            position[0] += (ball_vel[0] * remaining_time)
            position[1] += (ball_vel[1] * remaining_time)
            remaining_time = 0
            break

        #Colisiones y rebote con los margenes
        if t_min is not None and t_min[0] == "t_margin":
            #Posicionamiento de la bola cuando colisiona    
            position[0] += ball_vel[0] * t_min[1]
            position[1] += ball_vel[1] * t_min[1]

            #Inveriosn de la direccion de la bola
            ball_vel[1] = -ball_vel[1]

            #Calculo del tiempo del restante del frame
            remaining_time -= t_min[1]
            continue

        #Colision con Pala1
        elif t_min is not None and t_min[0] == "t_pala1":
            #Posicionamiento de la bola cuando colisiona    
            position[0] += ball_vel[0] * t_min[1]
            position[1] += ball_vel[1] * t_min[1]
            
            #Ajuste de la velocidad y del angulo del rebote 
            coll_point_y = relative_collision_point(position[1], pala1.centery, pala1.height)
            bounce_angle = coll_point_y * max_bounce_angle
            bounce_angle_rad = math.radians(bounce_angle)
            if (ball_speed * 1.1) <= 700:
                ball_speed *= 1.1 
            ball_vel[0] = ball_speed * math.cos(bounce_angle_rad)
            ball_vel[1] = ball_speed * math.sin(bounce_angle_rad)
            
            #Calculo del tiempo del restante del frame
            remaining_time -= t_min[1]
            continue
        #Colision con pala2
        elif t_min is not None and t_min[0] == "t_pala2":
            #Posicionamiento de la bola cuando colisiona
            position[0] += ball_vel[0] * t_min[1]
            position[1] += ball_vel[1] * t_min[1]

            #Ajuste de la velocidad y del angulo del rebote 
            coll_point_y = relative_collision_point(position[1], pala2.centery, pala2.height)
            bounce_angle = coll_point_y * max_bounce_angle
            bounce_angle_rad = math.radians(bounce_angle) 
            if (ball_speed * 1.05) <= 650:
                ball_speed *= 1.05
            ball_vel[0] = - ball_speed * math.cos(bounce_angle_rad)
            ball_vel[1] = ball_speed * math.sin(bounce_angle_rad)
            
            #Calculo del tiempo del restante del frame
            remaining_time -= t_min[1]
            continue
        
    ball_real = position[:]
    #Deteccion de puntos y reinicio de la posicion de la bola
    if ball_real[0] < 0:
        p2_score += 1
        ball_vel = [0,0]
        ball_real = [width / 2, height / 2]
        ball_render = ball_real[:]
        service = False
        ball_speed = ball_reset_speed
        #print(f"{p1_name} - {p1_score}     {p2_name} - {p2_score}")
    elif ball_real[0] > width:
        p1_score += 1
        ball_vel = [0,0]
        ball_real = [width / 2, height / 2]
        ball_render = ball_real[:]
        service = True
        ball_speed = ball_reset_speed
        #print(f"{p1_name} - {p1_score}     {p2_name} - {p2_score}")

    #Marcador
    scores_text = f"{p1_name} - {p1_score}   {p2_name} - {p2_score}"
    scoreboard = font.render(scores_text, True, (0, 0, 0), (255, 255, 255))
    

    alpha = 0.8
    ball_render[0] += (ball_real[0] - ball_render[0]) * alpha
    ball_render[1] += (ball_real[1] - ball_render[1]) * alpha
    ball_center = (int(ball_render[0]), int(ball_render[1]))
    screen.fill((0,0,0))

    #Dibuja las palas
    pygame.draw.rect(screen, (255,255,255), pala1)
    pygame.draw.rect(screen, (255,255,255), pala2)
    pygame.draw.circle(screen, (255,255,255), ball_center, BALL_RADIUS)
    screen.blit(scoreboard, (width//2 - scoreboard.get_width()//2, 20))

    #Actualiza la screen
    pygame.display.flip()

    


#Desinicializacion de pygame
pygame.quit()
