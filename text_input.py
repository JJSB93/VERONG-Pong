import pygame

class TextInput:
    def __init__(self, manager, relative_y=0):
        self.manager = manager
        self.relative_y = relative_y
        self.text = ""
        self.active = False
        self.width = 380
        self.height = 50
        self.padding = 10
        # Rect permanente usado para hit-testing y dibujo
        self.rect = pygame.Rect(0,0,self.width,self.height)
        # Caret
        self.caret_pos = 0
        self.caret_visible = True
        self.caret_timer = 0.0
        self.caret_blink_period = 0.5
        self.max_length = 19

    def update(self, delta_time):
        # actualizar la posición de self.rect
        self.rect.centerx = self.manager.width // 2
        self.rect.centery = self.manager.menu_center_y + self.relative_y

        # Actualizar el caret
        self.caret_timer += delta_time
        if self.caret_timer >= self.caret_blink_period:
            self.caret_visible = not self.caret_visible
            self.caret_timer = 0.0


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.caret_timer = 0
                self.caret_visible = True
            else:
                self.active = False

        # Procesar teclas
        if event.type == pygame.KEYDOWN and self.active:
            self.caret_timer = 0
            self.caret_visible = True

            if event.key == pygame.K_BACKSPACE:
                if self.text and self.caret_pos > 0:
                    self.text = self.text[:self.caret_pos-1] + self.text[self.caret_pos:]
                    self.caret_pos -= 1
            elif event.key == pygame.K_DELETE:
                if self.caret_pos < len(self.text):
                    self.text = self.text[:self.caret_pos] + self.text[self.caret_pos+1:]
            elif event.key == pygame.K_LEFT:
                if self.caret_pos > 0:
                    self.caret_pos -= 1
            elif event.key == pygame.K_RIGHT:
                if self.caret_pos < len(self.text):
                    self.caret_pos += 1 
            elif event.unicode.isprintable():
                if len(self.text) < self.max_length:
                    self.text = self.text[:self.caret_pos] + event.unicode + self.text[self.caret_pos:]
                    self.caret_pos += 1
            


    def draw(self):

        if self.active:
            bg_color = self.manager.LIGHT_GRAY
        else:
            bg_color = self.manager.GRAY

        pygame.draw.rect(self.manager.screen, bg_color, self.rect)
        
        if self.active:
            border_color = self.manager.HIGHLIGHT
        else:
            border_color = self.manager.GRAY

        pygame.draw.rect(self.manager.screen, border_color, self.rect, width=2)

        text_surface = self.manager.font_text.render(self.text, True, self.manager.TXT_RED)

        text_rect = text_surface.get_rect()
        text_rect.left = self.rect.left + self.padding
        text_rect.centery = self.rect.centery

        self.manager.screen.blit(text_surface, text_rect)

        if self.active and self.caret_visible:
            width = self.manager.font_text.size(self.text[:self.caret_pos])[0]
            caret_x = text_rect.left + width
            pygame.draw.line(
                self.manager.screen,
                self.manager.BLACK,
                 (caret_x, text_rect.top + self.padding),
                 (caret_x, text_rect.bottom - self.padding))


