import pygame

class TextInput:
    def __init__(self, manager, relative_y=0):
        self.manager = manager
        self.relative_y = relative_y
        self.text = ""
        self.active = False
        self.width = 300
        self.height = 50
        # Rect permanente usado para hit-testing y dibujo
        self.rect = pygame.Rect(0,0,self.width,self.height)
        # Caret
        self.caret_pos = 0
        self.caret_visible = True
        self.caret_timer = 0.0
        self.caret_blink_period = 0.5
        self.max_length = 25

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # actualizar la posición del rect antes de probar el click
            self.rect.centerx = self.manager.width // 2
            self.rect.centery = self.manager.menu_center_y + self.relative_y
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False


    def draw(self):
        center_y = self.manager.menu_center_y + self.relative_y
        x = self.manager.width // 2 - self.width // 2
        y = center_y - self.height // 2
        # sincronizar el rect con la posicion usada para dibujar
        self.rect.topleft = (x, y)
        if self.active:
            bg_color = self.manager.LIGHT_GRAY
        else:
            bg_color = self.manager.GRAY

        pygame.draw.rect(self.manager.screen, bg_color, (x, y, self.width, self.height))
        
        if self.active:
            border_color = self.manager.HIGHLIGHT
        else:
            border_color = self.manager.GRAY

        pygame.draw.rect(self.manager.screen, border_color, (x, y, self.width, self.height), width=2)

        text_surface = self.manager.font.render(self.text, True, self.manager.WHITE)

        self.text_rect = text_surface.get_rect()
        self.text_rect.center = (x + self.width // 2, y + self.height // 2)

        self.manager.screen.blit(text_surface, self.text_rect)

