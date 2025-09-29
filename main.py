import pygame, sys, json
from game.gestor_views import GestorViews
from game.views.menu import Menu

def main():
    pygame.init()

    # ----------------------------
    # Cargar configuración una sola vez
    # ----------------------------
    with open("config/config.json", "r") as f:
        CONFIG = json.load(f)

    pantalla = pygame.display.set_mode(
        (CONFIG["ancho_pantalla"], CONFIG["alto_pantalla"])
    )
    pygame.display.set_caption("Juego con Escenas")

    # Fondo menú desde CONFIG
    fondo_menu = pygame.image.load(CONFIG["fondos"]["menu"]).convert()
    fondo_menu = pygame.transform.scale(
        fondo_menu,
        (CONFIG["ancho_pantalla"], CONFIG["alto_pantalla"])
    )

    reloj = pygame.time.Clock()

    # Gestor de escenas
    manager = GestorViews()
    # Pasamos CONFIG al inicializar la escena
    manager.cambiar_escena(Menu(manager, CONFIG, fondo_menu))

    while True:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        manager.manejar_eventos(eventos)
        manager.actualizar()
        manager.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
