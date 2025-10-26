import pygame, math
from game_data import GameData
from button import Button

class GameStateManager:
    def __init__(self, screen, width, height, ball_reset_speed):
        
        self.width = width
        self.height = height
        self.screen = screen
        self.resolution = [width, height]
        self.ball_reset_speed = ball_reset_speed

        #Colores
        self.WHITE = (255, 255, 255)
        self.GRAY = (180, 180, 180)
        self.HIGHLIGHT = (255, 255, 100)

        #Medidas para colocar el menu
        self.spacing = 50
        self.title_y = 90
        self.menu_center_y = self.height // 2

        #Inicializacion de la fuente para el texto 
        self.font = pygame.font.SysFont("Arial", 38)
        self.font_title = pygame.font.SysFont("consolas", 120, bold=True)
        self.font_big = pygame.font.SysFont("Arial", 45)

        self.game_data = GameData(width, height, ball_reset_speed)

        self.game_states = {

            "menu": MenuState(self),
            "playing": PlayingState(self),
            "paused": PausedState(self)
        }

        self.current_state = "menu"

    def change_state(self, new_state_name):

        if new_state_name in self.game_states:
            self.current_state = new_state_name
        else:
            print(f"Error el estado {new_state_name} no existe")

    def handle_event(self, event):

        if self.current_state:
            current = self.game_states[self.current_state]
            current.handle_event(event)

        if event.type == pygame.VIDEORESIZE:
            self.width, self.height = event.w, event.h
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            if self.current_state == "menu":
                self.game_states["menu"].resize(self.width, self.height)
            

    def update(self, delta_time):

        if self.current_state:
            current = self.game_states[self.current_state]
            current.update(delta_time)

    def draw(self):

        if self.current_state:
            current = self.game_states[self.current_state]
            current.draw()


class MenuState:
    def __init__(self, manager):
        self.manager = manager
        self.screen = manager.screen
        self.width = manager.width
        self.height = manager.height

        #Render del titulo
        self.menu_title = "V  E  R  O  N  G"
        self.menu_title_render = self.manager.font_title.render(self.menu_title, True, self.manager.WHITE)

        self.button_play = None
        self.button_exit = None

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                self.manager.change_state("playing")

            elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

    def update(self, delta_time):
        if self.button_play == None:
            self.button_play = Button("Jugar", self.manager.menu_center_y , self.manager.font_big, self.manager.WHITE, self.manager.HIGHLIGHT, fade_enabled=True)
            self.button_exit = Button("Salir", self.manager.menu_center_y + 240, self.manager.font, self.manager.WHITE, self.manager.HIGHLIGHT)

        #Captura de la posicion y del clic del mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        #Actualizacion de los botones
        self.button_play.update(mouse_pos, mouse_click, delta_time, self.manager.width)
        self.button_exit.update(mouse_pos, mouse_click, delta_time, self.manager.width)

        if self.button_play.is_clicked():
            self.manager.change_state("playing")

        if self.button_exit.is_clicked():
            pygame.quit()
            exit()
        

    def draw(self):

        #Vaciado de la pantalla
        self.screen.fill((0, 0, 0))

        #Se dibujan los botones
        self.button_play.draw(self.screen)
        self.button_exit.draw(self.screen)

        #Blit del titulo
        self.screen.blit(self.menu_title_render, ((self.width //2) - (self.menu_title_render.get_width() //2), self.manager.title_y))

        #Actualizacion de la pantalla
        pygame.display.flip()

    def resize(self, width, height):
        self.width, self.height = width, height
        self.menu_center_y = height // 2
        self.menu_title_render = self.manager.font_title.render(self.menu_title, True, self.manager.WHITE)
        
        if self.button_play is not None:
            self.button_play = Button("Jugar", self.menu_center_y, self.manager.font_big, self.manager.WHITE, self.manager.HIGHLIGHT, fade_enabled=True)
            self.button_exit = Button("Salir", self.menu_center_y + 240, self.manager.font, self.manager.WHITE, self.manager.HIGHLIGHT)

class PlayingState:
    def __init__(self, manager):
        self.manager = manager

        #Posicion incial, tamano e inicializacion de las palas como rect
        self.pala_height = 100
        self.pala_width = 20

        self.pala1_x = int(self.manager.width * 0.15)
        self.pala2_x = int(self.manager.width - (self.manager.width * 0.15) - self.pala_width)

        self.pala1_y = int((self.manager.height * 0.5) - (self.pala_height / 2))
        self.pala2_y = int((self.manager.height * 0.5) - (self.pala_height / 2))

        self.pala1 = pygame.Rect(self.pala1_x, self.pala1_y, self.pala_width, self.pala_height)
        self.pala2 = pygame.Rect(self.pala2_x, self.pala2_y, self.pala_width, self.pala_height)

        self.pala1_y_real = self.pala1.y
        self.pala2_y_real = self.pala2.y

        #Posicion inicial de la bola e inicializacion de la velocidad
        self.EPSILON = 1e-9
        self.BALL_RADIUS = 10
        self.ball_center = (self.manager.width * 0.5, self.manager.height * 0.5)
        self.manager.game_data.ball_real = list(self.ball_center)
        self.ball_render = self.manager.game_data.ball_real[:]
        self.manager.game_data.ball_vel = [0, 0]
        self.manager.game_data.ball_speed = 400
        self.paddle_speed = 350

        #Rango del angulo de rebote 
        self.max_bounce_angle = 45
        self.b_angle_rad = 0.0

        #Inicializacion del saque y de la variable que almacena la colision mas cercana
        self.service = False
        self.t_min = None

##Funciones para detectar colision matematica
    #Calcula el momento en el que ocurre la colision
    def collision_x(self, x, vx, pala_edge): 
        if vx > 0:
            t = (pala_edge - self.BALL_RADIUS - x) / vx
            return t
        elif vx < 0:
            t = (pala_edge + self.BALL_RADIUS - x) / vx
            return t
        elif vx == 0:
            return None
    
    #Comprueba si en el momento "t", la pala colisiona con "y"
    def collision_y_check(self, y, vy, pala_rect, t): 
        top = pala_rect.top
        bottom = pala_rect.bottom
        y_in_collision = y + vy * t
        return  top - self.BALL_RADIUS <= y_in_collision <= bottom + self.BALL_RADIUS

    #Comprueba si hay colision con la pala y devuelve el momento dentro del frame donde ocurre la colision "t"
    def collision_detection(self, position, pala_rect):  
        x, y = position       
        vx, vy = self.manager.game_data.ball_vel     
        # La bola se mueve hacia la izquierda
        if vx < 0:
            t = self.collision_x(x, vx, pala_rect.right)
            if t > 0 and self.collision_y_check(y, vy, pala_rect, t):
                return t
        # La bola se mueve hacia la derecha    
        elif vx > 0:
            t = self.collision_x(x, vx, pala_rect.left)
            if t > 0 and self.collision_y_check(y, vy, pala_rect, t):
                return t

        return None
    
    #Funcion para calcular la distancia entre la colision y el centro de la pala
    def relative_collision_point(self, position_y, pala_center_y, pala_height):
        relative_y = (position_y - pala_center_y)
        normalized_y = relative_y / (pala_height / 2)
        return max(-1,min(normalized_y, 1))
    
    #Funcion para el calculo del momento de colision "t" con los bordes
    def margins_collision(self, y):
        vy = self.manager.game_data.ball_vel[1]
        if vy > 0:
            t = (self.manager.height - self.BALL_RADIUS - y) / vy
            return t
        elif vy < 0:
            t = (self.BALL_RADIUS - y) / vy
            return t
        elif vy == 0:
            return None
##

    def handle_event(self, event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.change_state("paused")
            elif event.key == pygame.K_g:
                if self.manager.game_data.ball_vel[0] == 0:
                    self.manager.game_data.ball_vel[0] = self.manager.game_data.ball_reset_speed if self.service else -self.manager.game_data.ball_reset_speed
    
    def update(self, delta_time):

        #Registrar teclas pulsadas y mover las palas
        keys_state = pygame.key.get_pressed()
        if keys_state[pygame.K_w]:
            self.pala1_y_real -= self.paddle_speed * delta_time
        elif keys_state[pygame.K_s]:
            self.pala1_y_real += self.paddle_speed * delta_time

        if keys_state[pygame.K_UP]:
            self.pala2_y_real -= self.paddle_speed * delta_time
        elif keys_state[pygame.K_DOWN]:
            self.pala2_y_real += self.paddle_speed * delta_time

        #Limitar el movimiento de las palas a los bordes 
        if self.pala1_y_real < 0:
            self.pala1_y_real = 0
        if self.pala1_y_real > self.manager.height - self.pala1.height:
            self.pala1_y_real = self.manager.height - self.pala1.height

        if self.pala2_y_real < 0:
            self.pala2_y_real = 0
        if self.pala2_y_real > self.manager.height - self.pala2.height:
            self.pala2_y_real = self.manager.height - self.pala2.height

        #Actualizar la posicion de pala.y mediante una variable
        # para poder aumentar y disminuir en decimales
        self.pala1.y = int(self.pala1_y_real)
        self.pala2.y = int(self.pala2_y_real)

        remaining_time = delta_time
        position = self.manager.game_data.ball_real[:]
        while remaining_time > self.EPSILON:
            #Calcular los timepos de colision
            collision_times = []
            collision_times_filtered = []
            t_min = None
            t_pala1 = self.collision_detection(position, self.pala1)
            t_pala2 = self.collision_detection(position, self.pala2)
            t_margin = self.margins_collision(position[1])

            #Calcular la colision mas proxima en el tiempo
            collision_times = [("t_pala1", t_pala1), ("t_pala2", t_pala2), ("t_margin", t_margin)]

            for collision in collision_times:
                if collision[1] is not None and self.EPSILON < collision[1] <= (remaining_time - self.EPSILON):
                    collision_times_filtered.append(collision)
            
            for collision in collision_times_filtered:
                if t_min == None or collision[1] < t_min[1]:
                    t_min = collision

            if t_min == None:
                position[0] += (self.manager.game_data.ball_vel[0] * remaining_time)
                position[1] += (self.manager.game_data.ball_vel[1] * remaining_time)
                remaining_time = 0
                break

            #Colisiones y rebote con los margenes
            if t_min is not None and t_min[0] == "t_margin":
                #Posicionamiento de la bola cuando colisiona    
                position[0] += self.manager.game_data.ball_vel[0] * t_min[1]
                position[1] += self.manager.game_data.ball_vel[1] * t_min[1]

                #Inveriosn de la direccion de la bola
                self.manager.game_data.ball_vel[1] = -self.manager.game_data.ball_vel[1]

                #Calculo del tiempo del restante del frame
                remaining_time -= t_min[1]
                continue

            #Colision con Pala1
            elif t_min is not None and t_min[0] == "t_pala1":
                #Posicionamiento de la bola cuando colisiona    
                position[0] += self.manager.game_data.ball_vel[0] * t_min[1]
                position[1] += self.manager.game_data.ball_vel[1] * t_min[1]
                
                #Ajuste de la velocidad y del angulo del rebote 
                coll_point_y = self.relative_collision_point(position[1], self.pala1.centery, self.pala1.height)
                bounce_angle = coll_point_y * self.max_bounce_angle
                bounce_angle_rad = math.radians(bounce_angle)
                if (self.manager.game_data.ball_speed * 1.05) <= 800:
                    self.manager.game_data.ball_speed *= 1.05 
                self.manager.game_data.ball_vel[0] = self.manager.game_data.ball_speed * math.cos(bounce_angle_rad)
                self.manager.game_data.ball_vel[1] = self.manager.game_data.ball_speed * math.sin(bounce_angle_rad)
                
                #Calculo del tiempo del restante del frame
                remaining_time -= t_min[1]
                continue

            #Colision con pala2
            elif t_min is not None and t_min[0] == "t_pala2":
                #Posicionamiento de la bola cuando colisiona
                position[0] += self.manager.game_data.ball_vel[0] * t_min[1]
                position[1] += self.manager.game_data.ball_vel[1] * t_min[1]

                #Ajuste de la velocidad y del angulo del rebote 
                coll_point_y = self.relative_collision_point(position[1], self.pala2.centery, self.pala2.height)
                bounce_angle = coll_point_y * self.max_bounce_angle
                bounce_angle_rad = math.radians(bounce_angle) 
                if (self.manager.game_data.ball_speed * 1.05) <= 800:
                    self.manager.game_data.ball_speed *= 1.05
                self.manager.game_data.ball_vel[0] = - self.manager.game_data.ball_speed * math.cos(bounce_angle_rad)
                self.manager.game_data.ball_vel[1] = self.manager.game_data.ball_speed * math.sin(bounce_angle_rad)
                
                #Calculo del tiempo del restante del frame
                remaining_time -= t_min[1]
                continue
        self.manager.game_data.ball_real = position[:]

        #Deteccion de puntos y reinicio de la posicion de la bola
        if self.manager.game_data.ball_real[0] < 0:
            self.manager.game_data.p2_score += 1
            self.manager.game_data.ball_vel = [0,0]
            self.manager.game_data.ball_real = [self.manager.width / 2, self.manager.height / 2]
            self.ball_render = self.manager.game_data.ball_real[:]
            self.service = False
            self.manager.game_data.ball_speed = self.manager.game_data.ball_reset_speed

        elif self.manager.game_data.ball_real[0] > self.manager.width:
            self.manager.game_data.p1_score += 1
            self.manager.game_data.ball_vel = [0,0]
            self.manager.game_data.ball_real = [self.manager.width / 2, self.manager.height / 2]
            self.ball_render = self.manager.game_data.ball_real[:]
            self.service = True
            self.manager.game_data.ball_speed = self.manager.game_data.ball_reset_speed


    def draw(self):
        self.manager.screen.fill((0, 0, 0))  # ← Pantalla negra temporal

        #Marcador
        scores_text = f"{self.manager.game_data.p1_name} - {self.manager.game_data.p1_score}   {self.manager.game_data.p2_name} - {self.manager.game_data.p2_score}"
        scoreboard = self.manager.font.render(scores_text, True, (0, 0, 0), self.manager.WHITE)

        #Interpolacion del renderizado de la bola para suavizar el movimiento
        alpha = 0.8
        ball_render = self.manager.game_data.ball_real[:]
        ball_render[0] += (self.manager.game_data.ball_real[0] - ball_render[0]) * alpha
        ball_render[1] += (self.manager.game_data.ball_real[1] - ball_render[1]) * alpha
        
        ball_center = (int(ball_render[0]), int(ball_render[1]))

        pygame.draw.rect(self.manager.screen, self.manager.WHITE, self.pala1)
        pygame.draw.rect(self.manager.screen, self.manager.WHITE, self.pala2)
        pygame.draw.circle(self.manager.screen, self.manager.WHITE, ball_center, self.BALL_RADIUS)
        self.manager.screen.blit(scoreboard, (self.manager.width//2 - scoreboard.get_width()//2, 20))
        pygame.display.flip()

class PausedState:
    def __init__(self, manager):
        self.manager = manager
    def handle_event(self, event):
        pass
    def update(self, delta_time):
        pass
    def draw(self):
        self.manager.screen.fill((0, 0, 0))  # ← Pantalla negra temporal
        pygame.display.flip()