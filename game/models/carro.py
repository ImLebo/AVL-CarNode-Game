import pygame
import json

class Carro:
    def __init__(self, config_path: str):
        # Cargar configuración desde JSON
        with open(config_path, "r") as f:
            data = json.load(f)

        self.x = data["x"]
        self.y = data["y"]
        self.ancho = data["ancho"]
        self.alto = data["alto"]
        self.energia = data["energia"]

        self.velocidad_y = data["velocidad_y"]
        self.salto_impulso = data["salto_impulso"]
        self.gravedad = data["gravedad"]

        # Cargar sprites
        self.sprite1 = pygame.image.load(data["sprites"]["frame1"]).convert_alpha()
        self.sprite2 = pygame.image.load(data["sprites"]["frame2"]).convert_alpha()
        self.sprite_salto = pygame.image.load(data["sprites"]["salto"]).convert_alpha()

        # Ajustar tamaño de sprites
        self.sprite1 = pygame.transform.scale(self.sprite1, (self.ancho, self.alto))
        self.sprite2 = pygame.transform.scale(self.sprite2, (self.ancho, self.alto))
        self.sprite_salto = pygame.transform.scale(self.sprite_salto, (self.ancho, self.alto))

        # Estado del carro
        self.saltando = False
        self.velocidad_salto = 0
        self.frame_actual = 0
        self.contador_anim = 0

    #Manejo de colisiones más adelante
    def rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def mover(self, teclas):
        # Movimiento vertical
        if teclas[pygame.K_UP]:
            self.y -= self.velocidad_y
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidad_y

        # Salto
        if not self.saltando and teclas[pygame.K_SPACE]:
            self.saltando = True
            self.velocidad_salto = self.salto_impulso

    def actualizar(self, alto_pantalla):
        if self.saltando:
            self.y += self.velocidad_salto
            self.velocidad_salto += self.gravedad
            if self.y >= alto_pantalla - self.alto - 50:  # suelo
                self.y = alto_pantalla - self.alto - 50
                self.saltando = False

        # Actualizar animación (cambiar entre frame1 y frame2 cada 10 ticks)
        self.contador_anim += 1
        if self.contador_anim >= 10:
            self.frame_actual = (self.frame_actual + 1) % 2
            self.contador_anim = 0

    def dibujar(self, pantalla):
        if self.saltando:
            pantalla.blit(self.sprite_salto, (self.x, self.y))
        else:
            if self.frame_actual == 0:
                pantalla.blit(self.sprite1, (self.x, self.y))
            else:
                pantalla.blit(self.sprite2, (self.x, self.y))
