#Clase para los botones
class Button:
    def __init__(self, text, pos_y, font, color_normal, color_hover, fade_enabled=False):
        self.text = text
        self.pos_y = pos_y
        self.font = font
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.fade_enabled = fade_enabled

        self.alpha = 255
        self.fade_direction = -1
        self.fading_speed = 200

        self.base_surface = self.font.render(text, True, color_normal)
        self.hover_surface = self.font.render(text, True, color_hover)

        self.rect = self.base_surface.get_rect()
        self.rect.centery = pos_y +self.base_surface.get_height() // 2

        self.is_hovered = False
        self.clicked = False

    def update(self, mouse_pos, mouse_click, delta_time, screen_width):
        self.rect.centerx = screen_width // 2

        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
        if self.fade_enabled and not self.is_hovered:
            self.alpha += self.fade_direction * self.fading_speed * delta_time
            if self.alpha <= 100:
                self.alpha = 100
                self.fade_direction = 1
            elif self.alpha >= 255:
                self.alpha = 255
                self.fade_direction = -1
        
        if self.is_hovered:
            self.alpha = 255
        
        self.clicked = self.is_hovered and mouse_click

    def draw(self, screen):
        surface = self.hover_surface if self.is_hovered else self.base_surface
        render_surface = surface.copy()
        render_surface.set_alpha(int(self.alpha))

        screen.blit(render_surface, render_surface.get_rect(center=self.rect.center))

    def is_clicked(self):
        return self.clicked