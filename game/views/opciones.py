import pygame, json
from game.models.boton import Boton
from game.models.inputbox import InputBox

class Opciones:
    def __init__(self, manager, config):
        # Cargar configuración principal
        self.manager = manager
        self.config = config

        # Cargar configuración del carro
        with open("config/carro.json", "r") as f:
            self.carroconfig = json.load(f)

        self.fondo = pygame.Surface((config["ancho_pantalla"], config["alto_pantalla"]))
        self.fondo.fill((50, 50, 50))

        # InputBox para configuraciones generales
        self.inputs = {
            "avance_px": InputBox(300, 150, 140, 40, config["avance_px"]),
            "intervalo_ms": InputBox(300, 200, 140, 40, config["intervalo_ms"]),
            "distancia_m": InputBox(300, 250, 140, 40, config["distancia_m"])
        }

        # InputBox para configuraciones del carro
        self.inputcarro = {
            "salto_impulso": InputBox(300, 300, 140, 40, self.carroconfig["salto_impulso"])
        }

        # Botones
        self.btn_guardar = Boton(300, 380, 200, 60, "assets/UI/btn_guardar.png", "guardar", None)
        self.btn_volver = Boton(300, 460, 200, 60, "assets/UI/btn_volver.png", "volver", None)

    def iniciar(self):
        print("Escena: Opciones")

    def manejar_eventos(self, eventos):
        for evento in eventos:
            for inputbox in self.inputs.values():
                inputbox.manejar_evento(evento)
            for inputbox in self.inputcarro.values():
                inputbox.manejar_evento(evento)

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.btn_guardar.rect.collidepoint(evento.pos):
                    self.guardar_config()
                elif self.btn_volver.rect.collidepoint(evento.pos):
                    from game.views.menu import Menu
                    fondo = pygame.image.load(self.config["fondos"]["menu"]).convert()
                    fondo = pygame.transform.scale(fondo, (self.config["ancho_pantalla"], self.config["alto_pantalla"]))
                    self.manager.cambiar_escena(Menu(self.manager, self.config, fondo))

    def actualizar(self):
        for inputbox in self.inputs.values():
            inputbox.actualizar()
        for inputbox in self.inputcarro.values():
            inputbox.actualizar()

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        fuente = pygame.font.SysFont(None, 36)

        # Config general
        y = 150
        for clave, inputbox in self.inputs.items():
            texto = fuente.render(clave, True, (255, 255, 255))
            pantalla.blit(texto, (150, y+10))
            inputbox.dibujar(pantalla)
            y += 50

        # Config carro
        for clave, inputbox in self.inputcarro.items():
            texto = fuente.render(clave, True, (255, 255, 255))
            pantalla.blit(texto, (150, 300))
            inputbox.dibujar(pantalla)

        # Botones
        self.btn_guardar.pantalla = pantalla
        self.btn_guardar.dibujar_en_pantalla()
        self.btn_volver.pantalla = pantalla
        self.btn_volver.dibujar_en_pantalla()

    def guardar_config(self):
        # Guardar en config.json
        for clave, inputbox in self.inputs.items():
            self.config[clave] = inputbox.get_value()
        with open("config/config.json", "w") as f:
            json.dump(self.config, f, indent=4)

        # Guardar en carro.json
        for clave, inputbox in self.inputcarro.items():
            self.carroconfig[clave] = inputbox.get_value()
        with open("config/carro.json", "w") as f:
            json.dump(self.carroconfig, f, indent=4)

        print("Configuraciones guardadas:", self.config, self.carroconfig)
