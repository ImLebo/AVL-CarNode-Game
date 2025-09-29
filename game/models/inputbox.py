import pygame

class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactivo = (180, 180, 180)
        self.color_activo = (255, 255, 255)
        self.color = self.color_inactivo
        self.texto = str(text)
        self.fuente = pygame.font.SysFont(None, 30)
        self.txt_surface = self.fuente.render(self.texto, True, (0, 0, 0))
        self.activo = False

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Activar/desactivar input
            if self.rect.collidepoint(evento.pos):
                self.activo = not self.activo
            else:
                self.activo = False
            self.color = self.color_activo if self.activo else self.color_inactivo

        if evento.type == pygame.KEYDOWN and self.activo:
            if evento.key == pygame.K_RETURN:
                self.activo = False
                self.color = self.color_inactivo
            elif evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            else:
                if evento.unicode.isdigit():
                    self.texto += evento.unicode

            self.txt_surface = self.fuente.render(self.texto, True, (0, 0, 0))

    def actualizar(self):
        # Ajustar ancho dinámicamente
        width = max(100, self.txt_surface.get_width()+10)
        self.rect.w = width

    def dibujar(self, pantalla):
        pantalla.blit(self.txt_surface, (self.rect.x+20, self.rect.y+5))
        pygame.draw.rect(pantalla, self.color, self.rect, 2)

    def get_value(self):
        try:
            return int(self.texto)
        except:
            return 0
