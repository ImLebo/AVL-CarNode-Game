import pygame, json
from avl.arbol_avl import ArbolAVL
from avl.nodo import Nodo
from game.models.carro import Carro

class VentanaJuego:
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config

        # Fondo desde CONFIG
        ruta_fondo = config["fondos"]["juego"]
        self.fondo = pygame.image.load(ruta_fondo).convert()
        self.fondo = pygame.transform.scale(
            self.fondo,
            (config["ancho_pantalla"], config["alto_pantalla"])
        )

        # Árbol AVL
        self.arbol = ArbolAVL()
        self.cargar_obstaculos("config/obstaculos.json")

        # Carro (jugador)
        self.carro = Carro("config/carro.json")

        # Estado del mundo
        self.mundo_x = 0
        self.tiempo = 0

    def cargar_obstaculos(self, ruta_json):
        with open(ruta_json, "r") as f:
            data = json.load(f)

        for obs in data:
            nodo = Nodo(
                x1=obs["x1"], x2=obs["x2"],
                y1=obs["y1"], y2=obs["y2"],
                tipo=obs["tipo"]
            )
            self.arbol.insertar(nodo)

    def iniciar(self):
        print("Escena: Juego iniciada")

    def manejar_eventos(self, eventos):
        teclas = pygame.key.get_pressed()
        self.carro.mover(teclas)

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # volver al menú
                    from game.views.menu import Menu
                    fondo = pygame.image.load(self.config["fondos"]["menu"]).convert()
                    fondo = pygame.transform.scale(
                        fondo,
                        (self.config["ancho_pantalla"], self.config["alto_pantalla"])
                    )
                    self.manager.cambiar_escena(Menu(self.manager, self.config, fondo))

    def actualizar(self):
        self.tiempo += 1
        self.mundo_x += 2

        # Actualizar carro
        self.carro.actualizar()

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))

        # Dibujar obstáculos (por ahora inorden)
        visibles = self.arbol.inorden()
        for nodo in visibles:
            x = nodo.x1 - self.mundo_x
            y = nodo.y1
            w = nodo.x2 - nodo.x1
            h = nodo.y2 - nodo.y1
            rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(pantalla, (100, 100, 100), rect)

        # Dibujar carro
        self.carro.dibujar(pantalla)

        # HUD (tiempo)
        fuente = pygame.font.SysFont(None, 40)
        texto = fuente.render(f"Tiempo: {self.tiempo}", True, (255, 255, 255))
        pantalla.blit(texto, (10, 10))
