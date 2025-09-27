import pygame

class GameOver:
    def __init__(self, manager, fondo):
        self.manager = manager
        self.fondo = fondo

    def iniciar(self):
        print("Escena: Game Over")

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    from menu import Menu
                    fondo = pygame.image.load("assets/fondo_menu.png").convert()
                    fondo = pygame.transform.scale(fondo, (800, 600))
                    self.manager.cambiar_escena(Menu(self.manager, fondo))

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        fuente = pygame.font.SysFont(None, 60)
        texto = fuente.render("GAME OVER", True, (255, 0, 0))
        pantalla.blit(texto, (250, 300))
