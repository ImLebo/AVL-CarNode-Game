import pygame
class Boton:
    def __init__ (self, x, y, ancho, altura, imagen, nombre, pantalla):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.altura = altura
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(self.imagen, (ancho, self.altura))
        self.rect = self.imagen.get_rect(topleft = (x,y))
        self.nombre = nombre
        self.pantalla = pantalla
        self.clickeado = False

    def detectar_click(self):
        posicion_mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(posicion_mouse):
            if pygame.mouse.get_pressed()[0]:
                return self.nombre

    def dibujar_en_pantalla(self):
        self.pantalla.blit(self.imagen, (self.x, self.y))