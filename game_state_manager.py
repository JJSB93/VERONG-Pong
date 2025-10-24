import pygame
from game_data import GameData
from button import Button

class GameStateManager:
    def __init__(self, screen, width, height, ball_reset_speed):
        self.screen = screen
        self.width = width
        self.height = height
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
        

        self.button_play = Button("Jugar", self.menu_center_y, self.manager.font_big, self.manager.WHITE, self.manager.HIGHLIGHT, fade_enabled=True)
        self.button_exit = Button("Salir", self.menu_center_y + 240, self.manager.font, self.manager.WHITE, self.manager.HIGHLIGHT)

class PlayingState:
    def __init__(self, manager):
        self.manager = manager
    def handle_event(self, event):
        pass
    def update(self, delta_time):
        pass
    def draw(self):
        self.manager.screen.fill((0, 0, 0))  # ← Pantalla negra temporal
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