import pygame, json
from avl.arbol_avl import ArbolAVL
from avl.nodo import Nodo
from game.models.carro import Carro
from game.utils.graficador import GraficadorAVL
from game.utils.colisiones import GestorColisiones
import queue

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
        
        # Fondo de carretera
        self.carretera_alto = config["carretera"]["alto"]
        ruta_carretera = config["carretera"]["img"]
        self.carretera_img = pygame.image.load(ruta_carretera).convert_alpha()
        self.carretera_img = pygame.transform.scale(
            self.carretera_img,
            (config["ancho_pantalla"], config["carretera"]["alto"])
        )

        self.carretera_y = config["carretera"]["y"]
        
        # Offset de desplazamiento
        self.carretera_offset = 0
        self.velocidad_carretera = 5  # píxeles por frame

        # Árbol AVL
        self.arbol = ArbolAVL()
        self.cola_eventos = queue.Queue()
        self.cargar_obstaculos("config/obstaculos.json")
        self.graficador = GraficadorAVL(self.arbol, self.cola_eventos)
        self.graficador.start()

        # Carro (jugador)
        self.carro = Carro("config/carro.json")
        self.gestor_colisiones = GestorColisiones(self.arbol, self.carro, config, self.cola_eventos)

        # Estado del mundo
        self.mundo_x = 0
        self.tiempo = 0
        self.distancia_px_objetivo = config["distancia_m"]

        # Control de tiempo
        self.ultimo_avance = pygame.time.get_ticks()  # milisegundos iniciales

    def cargar_obstaculos(self, ruta_json):
        with open(ruta_json, "r") as f:
            data = json.load(f)

        for obs in data:
            nodo = Nodo(
                x1=obs["x1"], x2=obs["x2"],
                y1=obs["y1"], y2=obs["y2"],
                tipo=obs["tipo"],
                img=obs.get("img")  # ✅ la ruta del JSON
            )

            # 📌 Si tiene ruta de imagen, la cargamos de una vez
            if nodo.img:
                try:
                    w = nodo.x2 - nodo.x1
                    h = nodo.y2 - nodo.y1
                    imagen = pygame.image.load(nodo.img).convert_alpha()
                    nodo.img_surface = pygame.transform.scale(imagen, (w, h))
                except Exception as e:
                    print(f"⚠️ No se pudo cargar {nodo.img}: {e}")
                    nodo.img_surface = None
            else:
                nodo.img_surface = None

            self.arbol.insertar(nodo)

        if self.cola_eventos:
            self.cola_eventos.put("actualizar")


    def iniciar(self):
        print("Escena: Juego iniciada")

    def manejar_eventos(self, eventos):
        teclas = pygame.key.get_pressed()
        self.carro.mover(teclas, self.carretera_y, self.config["carretera"]["alto"])

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

        # Avance automático
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_avance >= self.config["intervalo_ms"]:
            self.mundo_x += self.config["avance_px"]
            self.ultimo_avance = ahora

        # Actualizar carro
        self.carro.actualizar()
        
        # Mover carretera
        self.carretera_offset = (self.carretera_offset + self.velocidad_carretera) % self.config["ancho_pantalla"]

        # Colisiones + limpieza de obstáculos
        gameover = self.gestor_colisiones.verificar(self.mundo_x)
        if gameover:
            print("💀 Game Over por energía agotada")
            from game.views.gameover import GameOver
            fondo = pygame.image.load(self.config["fondos"]["juego"]).convert()
            fondo = pygame.transform.scale(
                fondo,
                (self.config["ancho_pantalla"], self.config["alto_pantalla"])
            )
            self.manager.cambiar_escena(GameOver(self.manager, fondo))

        # Meta alcanzada
        if self.mundo_x >= self.distancia_px_objetivo:
            print("🏁 Meta alcanzada!")
            from game.views.end import End
            fondo = pygame.image.load(self.config["fondos"]["juego"]).convert()
            fondo = pygame.transform.scale(
                fondo,
                (self.config["ancho_pantalla"], self.config["alto_pantalla"])
            )
            self.manager.cambiar_escena(End(self.manager.pantalla, self.config["ancho_pantalla"], self.config["alto_pantalla"], fondo))


    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        
        # Dibujar carretera con scroll infinito
        pantalla.blit(self.carretera_img, (-self.carretera_offset, self.carretera_y))
        pantalla.blit(self.carretera_img, (self.config["ancho_pantalla"] - self.carretera_offset, self.carretera_y))

        
        if self.graficador.surface:
            pantalla.blit(self.graficador.surface, (500, 50))

        x_min = self.mundo_x
        x_max = self.mundo_x + self.config["ancho_pantalla"]

        # Obstáculos visibles en rango (versión iterativa)
        visibles = self.arbol.consulta_rango(x_min, x_max)

        for nodo in visibles:
            x = nodo.x1 - self.mundo_x
            y = nodo.y1
            w = nodo.x2 - nodo.x1
            h = nodo.y2 - nodo.y1
            rect = pygame.Rect(x, y, w, h)

            if nodo.img_surface:  # ✅ usamos la superficie precargada
                pantalla.blit(nodo.img_surface, (x, y))
            else:
                color = (255, 0, 0) if nodo.tipo == "meta" else (100, 100, 100)
                pygame.draw.rect(pantalla, color, rect)


        self.carro.dibujar(pantalla)

        # HUD
        fuente = pygame.font.SysFont(None, 40)
        distancia_recorrida_m = self.mundo_x
        texto = fuente.render(
            f"Distancia: {distancia_recorrida_m} m / {self.config['distancia_m']} m",
            True,
            (255, 255, 255)
        )
        pantalla.blit(texto, (10, 10))
