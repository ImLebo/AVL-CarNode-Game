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

        # 🔋 Cargar sprite de batería
        self.bateria_img = pygame.image.load("assets/sprites/carro/bateria.png").convert_alpha()
        self.bateria_img = pygame.transform.scale(self.bateria_img, (30, 30))  # tamaño fijo

        # Estado del carro
        self.saltando = False
        self.velocidad_salto = 0
        self.suelo_y = self.y
        
        self.frame_actual = 0
        self.contador_anim = 0

    #Manejo de colisiones más adelante
    def rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def mover(self, teclas, carretera_y, carretera_alto):
        # Movimiento vertical libre
        if teclas[pygame.K_UP]:
            self.y -= self.velocidad_y
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidad_y

        # 🔒 Limitar dentro de la carretera
        if not self.saltando:
            if self.y < carretera_y+15:
                self.y = carretera_y+15
            if self.y + self.alto > carretera_y + carretera_alto - 15:
                self.y = carretera_y + carretera_alto - self.alto - 15

        # Salto
        if not self.saltando and teclas[pygame.K_SPACE]:
            self.saltando = True
            self.velocidad_salto = self.salto_impulso
            self.suelo_y = self.y

    def actualizar(self):
        if self.saltando:
            self.y += self.velocidad_salto
            self.velocidad_salto += self.gravedad

            # Cuando vuelva al suelo de referencia
            if self.y >= self.suelo_y:
                self.y = self.suelo_y
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
                
        # 🔋 Dibujar energía (baterías) en la parte superior derecha
        for i in range(self.energia):
            pantalla.blit(self.bateria_img, (800 - (i+1)*35, 10))
