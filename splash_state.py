import pygame
import math

class SplashState:
    def __init__(self, manager):
        self.manager = manager
        self.timer = 0
        self.duration = 3000  # milisegundos
        self.font_large = pygame.font.SysFont("consolas", 100)
        self.font_small = pygame.font.Font(None, 40)
        self.fade_surface = pygame.Surface((manager.width, manager.height))
        self.fade_surface.fill((0, 0, 0))
        self.fade_alpha = 255  # empieza en negro total

    def on_enter(self):
        # Preparar el efecto de fade y superficie al entrar
        self.timer = 0
        self.fade_alpha = 255
        self.fade_surface = pygame.Surface((self.manager.width, self.manager.height))
        self.fade_surface.fill((0, 0, 0))

    def resize(self, w, h):
        # Rehacer la superficie del velo al nuevo tamaño
        self.fade_surface = pygame.Surface((w, h))
        self.fade_surface.fill((0, 0, 0))

    def handle_event(self, event):
        # Permitir saltar la splash si se pulsa cualquier tecla
        if event.type == pygame.KEYDOWN:
            self.manager.change_state("menu")

    def update(self, delta_time):
        self.timer += delta_time * 1000
        # Fade in (0-1000ms), mantener (1000-2500ms), fade out (2500-3000ms)
        if self.timer < 1000:
            self.fade_alpha = 255 - int((self.timer / 1000) * 255)
        elif self.timer > 2500:
            self.fade_alpha = int(((self.timer - 2500) / 500) * 255)
        else:
            self.fade_alpha = 0

        if self.timer >= self.duration:
            self.manager.change_state("menu")

    def draw(self):
        screen = self.manager.screen
        screen.fill((0, 0, 0))

        # Efecto de brillo pulsante
        pulse = int(200 + 55 * math.sin(self.timer / 300))
        color = (pulse, pulse, 255)

        title = self.font_large.render("VERONG", True, color)
        subtitle = self.font_small.render("Creado por JJSB", True, (200, 200, 200))

        screen.blit(title, (self.manager.width // 2 - title.get_width() // 2,
                            self.manager.height // 2 - 100))
        screen.blit(subtitle, (self.manager.width // 2 - subtitle.get_width() // 2,
                               self.manager.height // 2 + 50))

        # Dibujar el fade
        self.fade_surface.set_alpha(self.fade_alpha)
        screen.blit(self.fade_surface, (0, 0))
        # El flip se hace una sola vez por frame en el GameStateManager
