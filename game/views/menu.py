import pygame

class Menu:
    def __init__(self, manager, config, fondo):
        self.manager = manager
        self.config = config
        self.fondo = fondo

    def iniciar(self):
        print("Escena: Menú principal")

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Enter para jugar
                    from game.views.ventanajuego import VentanaJuego
                    self.manager.cambiar_escena(VentanaJuego(self.manager, self.config))

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        fuente = pygame.font.SysFont(None, 50)
        texto = fuente.render("Presiona ENTER para Jugar", True, (255, 255, 255))
        pantalla.blit(texto, (100, 300))