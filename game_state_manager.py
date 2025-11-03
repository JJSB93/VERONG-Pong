import pygame, math
from game_data import GameData
from button import Button
from text_input import TextInput
from splash_state import SplashState

class GameStateManager:
    def __init__(self, screen, width, height, ball_reset_speed):
        
        self.width = width
        self.height = height
        self.screen = screen
        self.ball_reset_speed = ball_reset_speed

        #Colores
        self.WHITE = (255, 255, 255)
        self.GRAY = (180, 180, 180)
        self.LIGHT_GRAY = (211, 211, 211)
        self.HIGHLIGHT = (255, 255, 100)
        self.BLACK = (0, 0, 0)
        self.TXT_RED = (166, 75, 51)

        #Medidas para colocar el menu
        self.spacing = 50
        self.title_y = 90
        self.menu_center_y = self.height // 2

        #Inicializacion de la fuente para el texto 
        self.font = pygame.font.SysFont("Arial", 38)
        self.font_text = pygame.font.SysFont("consolas", 32)
        self.font_title = pygame.font.SysFont("consolas", 120, bold=True)
        self.font_big = pygame.font.SysFont("Arial", 45)


        self.game_data = GameData(width, height, ball_reset_speed)

        self.game_states = {
            "splash": SplashState(self),
            "menu": MenuState(self),
            "name_input": NameInputState(self),
            "playing": PlayingState(self),
            "paused": PausedState(self)
        }

        self.current_state = "splash"

    def change_state(self, new_state_name):

        if new_state_name in self.game_states:
            self.current_state = new_state_name
            # Preparar el layout del nuevo estado antes del primer draw
            state = self.game_states[new_state_name]
            if hasattr(state, "on_enter"):
                state.on_enter()
        else:
            print(f"Error el estado {new_state_name} no existe")

    def handle_event(self, event):

        # Resize: actualizar ventana y pedir recolocar al estado activo
        if event.type == pygame.VIDEORESIZE:
            self.width, self.height = event.w, event.h
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            self.menu_center_y = self.height // 2
            state = self.game_states.get(self.current_state)
            if state and hasattr(state, "resize"):
                state.resize(self.width, self.height)
            

        # Pasar el evento al estado actual
        state = self.game_states.get(self.current_state)
        if state and hasattr(state, "handle_event"):
            state.handle_event(event)

    def update(self, delta_time):

        if self.current_state:
            current = self.game_states[self.current_state]
            current.update(delta_time)

    def draw(self):

        if self.current_state:
            current = self.game_states[self.current_state]
            current.draw()
        # Un único flip por frame para todos los estados
        pygame.display.flip()

class MenuState:
    def __init__(self, manager):
        self.manager = manager
        self.screen = manager.screen
        self.width = manager.width
        self.height = manager.height

        #Render del titulo
        self.menu_title = "V  E  R  O  N  G"
        self.menu_title_render = self.manager.font_title.render(self.menu_title, True, self.manager.WHITE)

        self.button_play = Button("Jugar", self.manager.menu_center_y , self.manager.font_big, self.manager.WHITE, self.manager.HIGHLIGHT, fade_enabled=True)
        self.button_exit = Button("Salir", self.manager.menu_center_y + 240, self.manager.font, self.manager.WHITE, self.manager.HIGHLIGHT)

    def on_enter(self):
        # Asegura colocación correcta antes del primer draw
        self.layout()

    def layout(self):
        # Centrar horizontalmente y posicionar vertical con pos_y actual
        if self.button_play is not None and hasattr(self.button_play, "rect"):
            self.button_play.rect.centerx = self.manager.width // 2
            self.button_play.rect.centery = self.manager.menu_center_y
        if self.button_exit is not None and hasattr(self.button_exit, "rect"):
            self.button_exit.rect.centerx = self.manager.width // 2
            self.button_exit.rect.centery = self.manager.menu_center_y + 240

    def handle_event(self, event):

        if self.button_play is not None:
            self.button_play.handle_event(event)
        if self.button_exit is not None:
            self.button_exit.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                self.manager.change_state("name_input")
            elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

    def update(self, delta_time):
        # if self.button_play == None:
        #     self.button_play = Button("Jugar", self.manager.menu_center_y , self.manager.font_big, self.manager.WHITE, self.manager.HIGHLIGHT, fade_enabled=True)
        #     self.button_exit = Button("Salir", self.manager.menu_center_y + 240, self.manager.font, self.manager.WHITE, self.manager.HIGHLIGHT)

        #Captura de la posicion del mouse
        mouse_pos = pygame.mouse.get_pos()

        #Actualizacion de los botones
        self.button_play.update(mouse_pos, delta_time, self.manager.width)
        self.button_exit.update(mouse_pos, delta_time, self.manager.width)

        if self.button_play.is_clicked():
            self.manager.change_state("name_input")

        if self.button_exit.is_clicked():
            pygame.quit()
            exit()
        

    def draw(self):
        #Vaciado de la pantalla
        self.manager.screen.fill(self.manager.BLACK)

        #Se dibujan los botones
        self.button_play.draw(self.manager.screen)
        self.button_exit.draw(self.manager.screen)

        #Blit del titulo
        self.manager.screen.blit(self.menu_title_render, ((self.manager.width //2) - (self.menu_title_render.get_width() //2), self.manager.title_y))

    def resize(self, width, height):
        self.width, self.height = width, height
        self.menu_center_y = height // 2
        self.menu_title_render = self.manager.font_title.render(self.menu_title, True, self.manager.WHITE)
        # Re-ubicar botones sin perder su estilo/estado visual
        self.layout()

class NameInputState:
    def __init__(self, manager):
        self.manager = manager

        self.button_continue = Button("Continuar", self.manager.menu_center_y + 240, self.manager.font, self.manager.WHITE, self.manager.HIGHLIGHT, fade_enabled=True)
        self.button_backto_menu = Button("Volver al menú", self.manager.menu_center_y + 300, self.manager.font, self.manager.WHITE, self.manager.HIGHLIGHT)

        self.input1 = TextInput(self.manager, relative_y=-60)
        self.input2 = TextInput(self.manager, relative_y=0)

    def on_enter(self):
        # Colocar inputs y botones antes del primer draw y reiniciar el caret visual
        self.layout()
        for inp in (self.input1, self.input2):
            inp.caret_timer = 0.0
            inp.caret_visible = True

    def layout(self):
        # Inputs centrados con offsets relativos
        if hasattr(self.input1, "rect"):
            self.input1.rect.centerx = self.manager.width // 2
            self.input1.rect.centery = self.manager.menu_center_y - 60
        if hasattr(self.input2, "rect"):
            self.input2.rect.centerx = self.manager.width // 2
            self.input2.rect.centery = self.manager.menu_center_y + 0
        # Botones: centrar X y respetar sus Y objetivo
        if hasattr(self.button_continue, "rect"):
            self.button_continue.rect.centerx = self.manager.width // 2
            self.button_continue.rect.centery = self.manager.menu_center_y + 240
        if hasattr(self.button_backto_menu, "rect"):
            self.button_backto_menu.rect.centerx = self.manager.width // 2
            self.button_backto_menu.rect.centery = self.manager.menu_center_y + 300

    def resize(self, width, height):
        # Recolocar todo al cambiar el tamaño de la ventana
        self.layout()

    def handle_event(self, event):
        # Reenviar eventos a inputs
        click_in_1 = self.input1.handle_event(event)
        click_in_2 = self.input2.handle_event(event)
        # Gestionar foco
        if click_in_1:
            self.input1.active = True
            self.input2.active = False
        elif click_in_2:
            self.input2.active = True
            self.input1.active = False
        # Reenviar eventos a botones
        self.button_continue.handle_event(event)
        self.button_backto_menu.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.manager.change_state("playing")
            elif event.key == pygame.K_ESCAPE:
                self.manager.game_data.reset(self.manager.width, self.manager.height)
                self.manager.change_state("menu")

    def update(self, delta_time):
        mouse_pos = pygame.mouse.get_pos()

        self.button_continue.update(mouse_pos, delta_time, self.manager.width)
        self.button_backto_menu.update(mouse_pos, delta_time, self.manager.width)

        self.input1.update(delta_time)
        self.manager.game_data.p1_name = self.input1.text
        self.input2.update(delta_time)
        self.manager.game_data.p2_name = self.input2.text

        if self.button_continue.is_clicked():
            self.manager.change_state("playing")

        if self.button_backto_menu.is_clicked():
            self.manager.game_data.reset(self.manager.width, self.manager.height)
            self.manager.change_state("menu")

    def draw(self):
        self.manager.screen.fill(self.manager.BLACK)
        
        self.input1.draw()
        self.input2.draw()
        self.button_continue.draw(self.manager.screen)
        self.button_backto_menu.draw(self.manager.screen)

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
        self.ball_center = [self.manager.width * 0.5, self.manager.height * 0.5]
        self.manager.game_data.ball_real = list(self.ball_center)
        self.ball_render = self.manager.game_data.ball_real[:]
        self.manager.game_data.ball_vel = [0, 0]
        self.manager.game_data.ball_speed = 400
        self.paddle_speed = 350

        #Rango del angulo de rebote 
        self.max_bounce_angle = 45

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
    def relative_collision_point(self, position_y, pala_center_y):
        relative_y = (position_y - pala_center_y)
        normalized_y = relative_y / (self.pala_height / 2)
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
                if collision[1] is not None and self.EPSILON < collision[1] <= (remaining_time + self.EPSILON):
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
                coll_point_y = self.relative_collision_point(position[1], self.pala1.centery)
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
                coll_point_y = self.relative_collision_point(position[1], self.pala2.centery)
                bounce_angle = coll_point_y * self.max_bounce_angle
                bounce_angle_rad = math.radians(bounce_angle) 
                if (self.manager.game_data.ball_speed * 1.05) <= 800:
                    self.manager.game_data.ball_speed *= 1.05
                self.manager.game_data.ball_vel[0] = - self.manager.game_data.ball_speed * math.cos(bounce_angle_rad)
                self.manager.game_data.ball_vel[1] = self.manager.game_data.ball_speed * math.sin(bounce_angle_rad)
                
                #Calculo del tiempo del restante del frame
                remaining_time -= t_min[1]
                continue
        # Comprobación de seguridad para evitar atravesar palas
        if (self.pala1.collidepoint(position[0] - self.BALL_RADIUS, position[1]) or 
            self.pala2.collidepoint(position[0] + self.BALL_RADIUS, position[1])):
            # Corregir posición y velocidad
            if position[0] < self.manager.width / 2:
                position[0] = self.pala1.right + self.BALL_RADIUS
                self.manager.game_data.ball_vel[0] = abs(self.manager.game_data.ball_vel[0])
            else:
                position[0] = self.pala2.left - self.BALL_RADIUS
                self.manager.game_data.ball_vel[0] = -abs(self.manager.game_data.ball_vel[0])

        self.manager.game_data.ball_real = position[:]
        self.ball_center = self.manager.game_data.ball_real

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
        self.manager.screen.fill(self.manager.BLACK)

        #Marcador
        scores_text = f"{self.manager.game_data.p1_name} - {self.manager.game_data.p1_score}   {self.manager.game_data.p2_name} - {self.manager.game_data.p2_score}"
        scoreboard = self.manager.font.render(scores_text, True, self.manager.BLACK, self.manager.WHITE)

        #Interpolacion del renderizado de la bola para suavizar el movimiento
        alpha = 0.8
        self.ball_render[0] += (self.manager.game_data.ball_real[0] - self.ball_render[0]) * alpha
        self.ball_render[1] += (self.manager.game_data.ball_real[1] - self.ball_render[1]) * alpha
        
        ball_center = (int(self.ball_render[0]), int(self.ball_render[1]))

        for y in range(0, self.manager.height, 40):
            pygame.draw.rect(self.manager.screen, self.manager.WHITE, 
                     (self.manager.width // 2 - 5, y, 5, 20))
        pygame.draw.rect(self.manager.screen, self.manager.WHITE, self.pala1)
        pygame.draw.rect(self.manager.screen, self.manager.WHITE, self.pala2)
        pygame.draw.circle(self.manager.screen, self.manager.WHITE, ball_center, self.BALL_RADIUS)
        self.manager.screen.blit(scoreboard, (self.manager.width//2 - scoreboard.get_width()//2, 20))

    def resize(self, width, height):
        self.pala1_x = int(width * 0.15)
        self.pala2_x = int(width - (width * 0.15) - self.pala_width)
        self.pala1_y = int((height * 0.5) - (self.pala_height / 2))
        self.pala2_y = int((height * 0.5) - (self.pala_height / 2))
        self.pala1 = pygame.Rect(self.pala1_x, self.pala1_y, self.pala_width, self.pala_height)
        self.pala2 = pygame.Rect(self.pala2_x, self.pala2_y, self.pala_width, self.pala_height)
        self.pala1_y_real = self.pala1.y
        self.pala2_y_real = self.pala2.y
        self.manager.game_data.ball_real = [width * 0.5, height * 0.5]
        self.ball_center = self.manager.game_data.ball_real[:]
        self.ball_render = self.manager.game_data.ball_real[:]
        self.manager.game_data.ball_vel = [0, 0]

class PausedState:
    def __init__(self, manager):
        self.manager = manager

        self.button_keep_playing = None
        self.button_backto_menu = None
        self.button_exit = None
        self.pause_buttons = []

        self.pause_title = self.manager.font_title.render("PAUSA", True, self.manager.WHITE)

    def on_enter(self):
        # Crear botones si no existen y colocarlos antes del primer draw
        if self.button_keep_playing is None:
            self.button_keep_playing = Button("Reanudar", self.manager.menu_center_y, self.manager.font, self.manager.WHITE, self.manager.HIGHLIGHT, fade_enabled=True)
            self.button_backto_menu = Button("Volver al menú", self.manager.menu_center_y + 80, self.manager.font, self.manager.WHITE, self.manager.HIGHLIGHT)
            self.button_exit = Button("Salir del juego", self.manager.menu_center_y + 240, self.manager.font, self.manager.WHITE, self.manager.HIGHLIGHT)
            self.pause_buttons = [self.button_keep_playing, self.button_backto_menu, self.button_exit]
        self.layout()

    def layout(self):
        # Centrar horizontalmente; respetar las Y definidas
        for btn in self.pause_buttons:
            if hasattr(btn, "rect"):
                btn.rect.centerx = self.manager.width // 2
        if hasattr(self.button_keep_playing, "rect"):
            self.button_keep_playing.rect.centery = self.manager.menu_center_y
        if hasattr(self.button_backto_menu, "rect"):
            self.button_backto_menu.rect.centery = self.manager.menu_center_y + 80
        if hasattr(self.button_exit, "rect"):
            self.button_exit.rect.centery = self.manager.menu_center_y + 240

    def resize(self, width, height):
        # Recolocar con el nuevo tamaño
        self.layout()

    def handle_event(self, event):
        if self.button_keep_playing is not None:
            self.button_keep_playing.handle_event(event)
        if self.button_backto_menu is not None:
            self.button_backto_menu.handle_event(event)
        if self.button_exit is not None:
            self.button_exit.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.change_state("playing")

    def update(self, delta_time):
        # Aquí solo hover/animación; los botones ya existen
        self.mouse_pos = pygame.mouse.get_pos()

        for button in self.pause_buttons:
            button.update(self.mouse_pos, delta_time, self.manager.width)

        if self.button_keep_playing.is_clicked():
            self.manager.change_state("playing")
        elif self.button_backto_menu.is_clicked():
            self.manager.game_data.reset(self.manager.width, self.manager.height)
            self.manager.change_state("menu")
        elif self.button_exit.is_clicked():
            pygame.quit()
            exit()

    def draw(self):
        self.manager.screen.fill(self.manager.BLACK)
        for button in self.pause_buttons:
            button.draw(self.manager.screen)
        self.manager.screen.blit(self.pause_title, (self.manager.width//2 - self.pause_title.get_width()//2, self.manager.title_y))