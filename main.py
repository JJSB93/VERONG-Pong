import pygame, math
from button import Button
from game_data import GameData

EPSILON = 1e-9
BALL_RADIUS = 10

#Colores
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
HIGHLIGHT = (255, 255, 100) 

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

def collision_detection(position, game_data, pala_rect, r): # <-- Comprueba si hay colision con la pala 
    x, y = position                                            # y devuelve el momento dentro del frame donde 
    vx, vy = game_data.ball_vel                                           # ocurre la colision "t"
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
def margins_collision(y, game_data, r, height):
    vy = game_data.ball_vel[1]
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
font_title = pygame.font.SysFont("consolas", 120, bold=True)
font_big = pygame.font.SysFont("Arial", 45)

#Declaro variables
width = 1900
height = 1080
resolution = (width, height)
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

#Inicializacion del reloj del juego
game_clock = pygame.time.Clock()

#Velocidad base de la bola
ball_reset_speed = 400

#Instancia de los datos del juego
game_data = GameData(width, height, ball_reset_speed)

#Posicion incial, tamano e inicializacion de las palas como rect
pala_height = 100
pala_width = 20

pala1_x = int(width * 0.15)
pala2_x = int(width - (width * 0.15) - pala_width)

pala1_y = int((height * 0.5) - (pala_height / 2))
pala2_y = int((height * 0.5) - (pala_height / 2))

pala1 = pygame.Rect(pala1_x, pala1_y, pala_width, pala_height)
pala2 = pygame.Rect(pala2_x, pala2_y, pala_width, pala_height)

pala1_y_real = pala1.y
pala2_y_real = pala2.y

#Posicion inicial de la bola e inicializacion de la velocidad
ball_center = (width * 0.5, height * 0.5)
game_data.ball_real = list(ball_center)
ball_render = game_data.ball_real[:]
game_data.ball_vel = [0, 0]
game_data.ball_speed = 400
paddle_speed = 350

#Rango del angulo de rebote 
max_bounce_angle = 45
b_angle_rad = 0.0

#Inicializacion del saque y de la variable que almacena la colision mas cercana
service = False
t_min = None

#Medidas para colocar el menu
spacing = 50
title_y = 90
menu_center_y = height // 2

#Estado al arrancar el juego
game_state = "menu"

#Nombres de jugadores
p1_name = "Vero"
p2_name = "Juan"

#Inicializacion de variables para los botones
button_play = None
button_exit = None

button_continue = None
button_backto_menu = None
button_quit_game = None

#Render del titulo
menu_title = "V  E  R  O  N  G"
menu_title_render = font_title.render(menu_title, True, WHITE)

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
                    button_play = None
                    button_exit = None
                    button_continue = None
                    button_backto_menu = None
                    button_quit_game = None
                    game_state = "paused"
                elif game_state == "paused":
                    game_state = "playing"

            elif event.key == pygame.K_g and game_state == "playing":
                if game_data.ball_vel[0] == 0:
                    game_data.ball_vel[0] = ball_reset_speed if service else -ball_reset_speed
            
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

            game_data.ball_real = [width * 0.5, height * 0.5]
            game_data.ball_vel = [0, 0]
            ball_center = game_data.ball_real[:]
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mouse_left_down = True
            else:
                mouse_left_down = False    

    #Bucle del menu principal
    if game_state == "menu":

        #Inicializacion de los botones 
        if button_play is None:
            button_play = Button("Jugar", menu_center_y , font_big, WHITE, HIGHLIGHT, fade_enabled=True)
            button_exit = Button("Salir", menu_center_y + 240, font, WHITE, HIGHLIGHT)

        #Vaciado de la pantalla
        screen.fill((0, 0, 0))

        #Captura de la posicion y del clic del mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        #Actualizacion de los botones
        button_play.update(mouse_pos, mouse_click, delta_time, width)
        button_exit.update(mouse_pos, mouse_click, delta_time, width)

        #Se dibujan los botones
        button_play.draw(screen)
        button_exit.draw(screen)

        #Blit del titulo
        screen.blit(menu_title_render, ((width //2) - (menu_title_render.get_width() //2), title_y))

        #Actualizacion de la pantalla
        pygame.display.flip()

        if button_play.is_clicked():
            game_state = "playing"

        if button_exit.is_clicked():
            running = False

    elif game_state == "playing":

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
        position = game_data.ball_real[:]
        while remaining_time > EPSILON:
            #Calcular los timepos de colision
            collision_times = []
            collision_times_filtered = []
            t_min = None
            t_pala1 = collision_detection(position, game_data, pala1, BALL_RADIUS)
            t_pala2 = collision_detection(position, game_data, pala2, BALL_RADIUS)
            t_margin = margins_collision(position[1], game_data, BALL_RADIUS, height)

            #Calcular la colision mas proxima en el tiempo
            collision_times = [("t_pala1", t_pala1), ("t_pala2", t_pala2), ("t_margin", t_margin)]

            for collision in collision_times:
                if collision[1] is not None and EPSILON < collision[1] <= (remaining_time - EPSILON):
                    collision_times_filtered.append(collision)
            
            for collision in collision_times_filtered:
                if t_min == None or collision[1] < t_min[1]:
                    t_min = collision

            if t_min == None:
                position[0] += (game_data.ball_vel[0] * remaining_time)
                position[1] += (game_data.ball_vel[1] * remaining_time)
                remaining_time = 0
                break

            #Colisiones y rebote con los margenes
            if t_min is not None and t_min[0] == "t_margin":
                #Posicionamiento de la bola cuando colisiona    
                position[0] += game_data.ball_vel[0] * t_min[1]
                position[1] += game_data.ball_vel[1] * t_min[1]

                #Inveriosn de la direccion de la bola
                game_data.ball_vel[1] = -game_data.ball_vel[1]

                #Calculo del tiempo del restante del frame
                remaining_time -= t_min[1]
                continue

            #Colision con Pala1
            elif t_min is not None and t_min[0] == "t_pala1":
                #Posicionamiento de la bola cuando colisiona    
                position[0] += game_data.ball_vel[0] * t_min[1]
                position[1] += game_data.ball_vel[1] * t_min[1]
                
                #Ajuste de la velocidad y del angulo del rebote 
                coll_point_y = relative_collision_point(position[1], pala1.centery, pala1.height)
                bounce_angle = coll_point_y * max_bounce_angle
                bounce_angle_rad = math.radians(bounce_angle)
                if (game_data.ball_speed * 1.05) <= 800:
                    game_data.ball_speed *= 1.05 
                game_data.ball_vel[0] = game_data.ball_speed * math.cos(bounce_angle_rad)
                game_data.ball_vel[1] = game_data.ball_speed * math.sin(bounce_angle_rad)
                
                #Calculo del tiempo del restante del frame
                remaining_time -= t_min[1]
                continue

            #Colision con pala2
            elif t_min is not None and t_min[0] == "t_pala2":
                #Posicionamiento de la bola cuando colisiona
                position[0] += game_data.ball_vel[0] * t_min[1]
                position[1] += game_data.ball_vel[1] * t_min[1]

                #Ajuste de la velocidad y del angulo del rebote 
                coll_point_y = relative_collision_point(position[1], pala2.centery, pala2.height)
                bounce_angle = coll_point_y * max_bounce_angle
                bounce_angle_rad = math.radians(bounce_angle) 
                if (game_data.ball_speed * 1.05) <= 800:
                    game_data.ball_speed *= 1.05
                game_data.ball_vel[0] = - game_data.ball_speed * math.cos(bounce_angle_rad)
                game_data.ball_vel[1] = game_data.ball_speed * math.sin(bounce_angle_rad)
                
                #Calculo del tiempo del restante del frame
                remaining_time -= t_min[1]
                continue
        game_data.ball_real = position[:]

        #Deteccion de puntos y reinicio de la posicion de la bola
        if game_data.ball_real[0] < 0:
            game_data.p2_score += 1
            game_data.ball_vel = [0,0]
            game_data.ball_real = [width / 2, height / 2]
            ball_render = game_data.ball_real[:]
            service = False
            game_data.ball_speed = ball_reset_speed

        elif game_data.ball_real[0] > width:
            game_data.p1_score += 1
            game_data.ball_vel = [0,0]
            game_data.ball_real = [width / 2, height / 2]
            ball_render = game_data.ball_real[:]
            service = True
            game_data.ball_speed = ball_reset_speed

        #Marcador
        scores_text = f"{p1_name} - {game_data.p1_score}   {p2_name} - {game_data.p2_score}"
        scoreboard = font.render(scores_text, True, (0, 0, 0), WHITE)
        
        #Interpolacion del renderizado de la bola para suavizar el movimiento
        alpha = 0.8
        ball_render[0] += (game_data.ball_real[0] - ball_render[0]) * alpha
        ball_render[1] += (game_data.ball_real[1] - ball_render[1]) * alpha
        ball_render = game_data.ball_real[:]
        ball_center = (int(ball_render[0]), int(ball_render[1]))

        #Dibuja las palas, la bola y el marcador
        screen.fill((0,0,0))
        pygame.draw.rect(screen, WHITE, pala1)
        pygame.draw.rect(screen, WHITE, pala2)
        pygame.draw.circle(screen, WHITE, ball_center, BALL_RADIUS)
        screen.blit(scoreboard, (width//2 - scoreboard.get_width()//2, 20))

    elif game_state == "paused":
        if button_continue == None:
            button_continue = Button("Reanudar", menu_center_y, font, WHITE, HIGHLIGHT, fade_enabled=True)
            button_backto_menu = Button("Volver al menú", menu_center_y + 80, font, WHITE, HIGHLIGHT)
            button_exit = Button("Salir del juego", menu_center_y + 240, font, WHITE, HIGHLIGHT)
        pause_buttons = [button_continue, button_backto_menu, button_exit]

        screen.fill((0, 0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for button in pause_buttons:
            button.update(mouse_pos, mouse_click, delta_time, width)
            button.draw(screen)

        if pause_buttons[0].is_clicked():
            game_state = "playing"
        elif pause_buttons[1].is_clicked():
            game_data.reset(width, height)
            button_play = None
            button_exit = None
            button_continue = None
            button_backto_menu = None
            button_quit_game = None
            game_state = "menu"
        elif pause_buttons[2].is_clicked():
            running = False

        pause_title = font_title.render("PAUSA", True, WHITE)
        screen.blit(pause_title, (width//2 - pause_title.get_width()//2, title_y))

        pygame.display.flip()

    #Actualiza la screen
    pygame.display.flip()

#Desinicializacion de pygame
pygame.quit()
