import pygame
from game.models.boton import Boton  # asumiendo que Boton vive en game/models/boton.py

class Menu:
    def __init__(self, manager, config, fondo):
        self.manager = manager
        self.config = config
        self.fondo = fondo
        self.botones = []

        # Crear botones desde config
        for b in config["botones"]:
            boton = Boton(
                x=b["x"], y=b["y"],
                ancho=b["ancho"], altura=b["alto"],
                imagen=b["imagen"], nombre=b["nombre"],
                pantalla=None  # se asigna en dibujar
            )
            self.botones.append(boton)

    def iniciar(self):
        print("Escena: Menú principal")

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for boton in self.botones:
                    accion = boton.detectar_click()
                    if accion:
                        if accion == "jugar":
                            from game.views.ventanajuego import VentanaJuego
                            self.manager.cambiar_escena(VentanaJuego(self.manager, self.config))
                        elif accion == "opciones":
                            from game.views.opciones import Opciones
                            self.manager.cambiar_escena(Opciones(self.manager, self.config))
                        elif accion == "salir":
                            pygame.quit()
                            import sys
                            sys.exit()

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        for boton in self.botones:
            boton.pantalla = pantalla
            boton.dibujar_en_pantalla()