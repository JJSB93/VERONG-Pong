import pygame, math

EPSILON = 1e-7
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

#Inicializa pygame y el titulo
pygame.init()
pygame.display.set_caption("Juego de Vero")

#Inicializacion de la fuente para el texto 
font = pygame.font.SysFont("Arial", 38)


#Declaro variables
width = 1900
height = 1080
resolution = (width, height)
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

pala_height = 100
pala_width = 20

pala1_x = int(width * 0.15)
pala2_x = int(width - (width * 0.15) - pala_width)

pala1_y = int((height * 0.5) - (pala_height / 2))
pala2_y = int((height * 0.5) - (pala_height / 2))

pala1 = pygame.Rect(pala1_x, pala1_y, pala_width, pala_height)
pala2 = pygame.Rect(pala2_x, pala2_y, pala_width, pala_height)

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
max_bounce_angle = 45
b_angle_rad = 0.0
t_min = None
p1_score = 0
p2_score = 0
service = False
spacing = 50
title_y = 90
menu_center_y = height // 2

#Colores
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
HIGHLIGHT = (255, 255, 100) 



p1_name = "Vero"
p2_name = "Juan"

game_state = "menu"
menu_text1 = "Bienvenido al Juego de Vero" 
menu_text2 = "Jugar" 
menu_text3 = "Salir"
text_fading = False
fading_speed = 255
text_alpha = 0

menu_text1_render = font.render(menu_text1, True, WHITE)
menu_text2_render = font.render(menu_text2, True, (255, 255, 255, 255))
menu_text2_render_hoover = font.render(menu_text2, True, HIGHLIGHT)
menu_text3_render = font.render(menu_text3, True, WHITE)

mouse_left_down = False

#Bucle del juego
running = True
while running:
    #Ajustar los fps
    delta_time = game_clock.tick_busy_loop(240) / 1000
    mouse_left_down = False
    #Captura de eventos y resolucion 
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                game_state = "playing"
            elif event.key == pygame.K_ESCAPE:
                if game_state == "menu":
                    running = False
                elif game_state == "playing":
                    game_state = "menu"
            elif event.key == pygame.K_g and game_state == "playing":
                if ball_vel[0] == 0:
                    ball_vel[0] = ball_reset_speed if service else -ball_reset_speed
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            resolution = (width, height)

            pala1.x = int(width * 0.15)
            pala2.x = int(width - (width * 0.15) - pala2.width)

            pala1_y_real = int((height * 0.5) - (pala_height / 2))
            pala2_y_real = int((height * 0.5) - (pala_height / 2))
            pala1.y = pala1_y_real
            pala2.y = pala2_y_real

            ball_real = [width * 0.5, height * 0.5]
            ball_center = ball_real[:]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mouse_left_down = True
            else:
                mouse_left_down = False    

    #Bucle del menu principal
    if game_state == "menu":
        screen.fill((0, 0, 0))

        #Bucle de interpolacion del parpadeo del texto
        if text_fading:
            text_alpha += fading_speed * delta_time
            if text_alpha >= 255:
                text_fading = False
        elif not text_fading:
            text_alpha -= fading_speed * delta_time
            if text_alpha <= 0:
                text_fading = True
        
        menu_height = menu_text2_render.get_height() + menu_text3_render.get_height() + (spacing * 2)

        #Inicializacion de las hitbox del menu
        menu_2_pos = (width //2) - (menu_text2_render.get_width() //2), menu_center_y - (menu_height // 2)
        menu_2_box = menu_text2_render.get_rect(topleft=menu_2_pos)
        menu_3_pos = (width //2) - (menu_text3_render.get_width() //2), \
                        (menu_center_y - (menu_height // 2)) + menu_text2_render.get_height() + spacing
        menu_3_box = menu_text3_render.get_rect(topleft=menu_3_pos)

        #Captura de la posicion del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = (mouse_x, mouse_y)

        #Bucle para el cambio de estilo en hoover de JUGAR
        is_hoovered_1 = menu_3_box.collidepoint(mouse_pos)
        is_hoovered_2 = menu_2_box.collidepoint(mouse_pos)
        if is_hoovered_2:
            current_surface = menu_text2_render_hoover
            screen.blit(current_surface, ((width //2) - (menu_text2_render.get_width() //2), menu_center_y - (menu_height // 2)))
        else:
            current_surface = menu_text2_render
            text_alpha = max(0, min(255, text_alpha))
            current_surface.set_alpha(int(text_alpha))
            screen.blit(current_surface, ((width //2) - (menu_text2_render.get_width() //2), menu_center_y - (menu_height // 2)))
        #Captura del clic en Jugar
        if mouse_left_down and is_hoovered_2:
            game_state = "playing"
        if mouse_left_down and is_hoovered_1:
            running = False

        #Blit del titulo
        screen.blit(menu_text1_render, ((width //2) - (menu_text1_render.get_width() //2), title_y))

        #Blit de SALIR
        screen.blit(menu_text3_render, ((width //2) - (menu_text3_render.get_width() //2), \
                        (menu_center_y - (menu_height // 2)) + menu_text2_render.get_height() + spacing))
        

    if game_state == "playing":
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
            
        #Deteccion de puntos y reinicio de la posicion de la bola
        ball_real = position[:]
        if ball_real[0] < 0:
            p2_score += 1
            ball_vel = [0,0]
            ball_real = [width / 2, height / 2]
            ball_render = ball_real[:]
            service = False
            ball_speed = ball_reset_speed
        elif ball_real[0] > width:
            p1_score += 1
            ball_vel = [0,0]
            ball_real = [width / 2, height / 2]
            ball_render = ball_real[:]
            service = True
            ball_speed = ball_reset_speed


        #Marcador
        scores_text = f"{p1_name} - {p1_score}   {p2_name} - {p2_score}"
        scoreboard = font.render(scores_text, True, (0, 0, 0), WHITE)
        
        #Interpolacion del renderizado de la bola para suavizar el movimiento
        alpha = 0.8
        ball_render[0] += (ball_real[0] - ball_render[0]) * alpha
        ball_render[1] += (ball_real[1] - ball_render[1]) * alpha
        ball_render = ball_real[:]
        ball_center = (int(ball_render[0]), int(ball_render[1]))


        #Dibuja las palas, la bola y el marcador
        screen.fill((0,0,0))
        pygame.draw.rect(screen, WHITE, pala1)
        pygame.draw.rect(screen, WHITE, pala2)
        pygame.draw.circle(screen, WHITE, ball_center, BALL_RADIUS)
        screen.blit(scoreboard, (width//2 - scoreboard.get_width()//2, 20))

        

    
    #Actualiza la screen
    pygame.display.flip()

#Desinicializacion de pygame
pygame.quit()
