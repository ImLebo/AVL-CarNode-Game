import pygame, json
import matplotlib.pyplot as plt
from io import BytesIO
import textwrap
from game.models.boton import Boton
from avl.arbol_avl import ArbolAVL
from avl.nodo import Nodo


class Recorridos:
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config
        self.arbol = ArbolAVL()
        self.cargar_arbol("config/obstaculos.json")
        self.fondo = pygame.Surface((config["ancho_pantalla"], config["alto_pantalla"]))
        self.fondo.fill((30, 30, 30))

        self.img_surface = None
        self.recorrido_actual = "inorden"  # por defecto
        self.generar_grafico(self.recorrido_actual)

        # Botones
        self.botones = {
            "preorden": Boton(50, 500, 150, 50, "assets/UI/btn_preorden.png", "preorden", None),
            "inorden": Boton(220, 500, 150, 50, "assets/UI/btn_inorden.png", "inorden", None),
            "postorden": Boton(390, 500, 150, 50, "assets/UI/btn_postorden.png", "postorden", None),
            "anchura": Boton(560, 500, 150, 50, "assets/UI/btn_anchura.png", "anchura", None),
        }

    def cargar_arbol(self, ruta_json):
        with open(ruta_json, "r") as f:
            data = json.load(f)

        for obs in data:
            nodo = Nodo(
                x1=obs["x1"], x2=obs["x2"],
                y1=obs["y1"], y2=obs["y2"],
                tipo=obs["tipo"]
            )
            self.arbol.insertar(nodo)

    def dibujar_arbol(self, nodo, x, y, dx, dy, ax):
        """
        Dibuja el árbol recursivamente en matplotlib.
        Cada nodo muestra (valor_x, valor_y).
        """
        if nodo is None:
            return

        # Dibujar nodo (círculo)
        ax.scatter(x, y, s=800, c="skyblue", edgecolors="black", zorder=2)
        ax.text(
            x, y, f"({nodo.valor_x},{nodo.valor_y})",
            fontsize=8, ha="center", va="center", zorder=3
        )

        # Dibujar hijo izquierdo
        if nodo.izquierdo:
            ax.plot([x, x - dx], [y, y - dy], c="black")
            self.dibujar_arbol(nodo.izquierdo, x - dx, y - dy, dx / 2, dy, ax)

        # Dibujar hijo derecho
        if nodo.derecho:
            ax.plot([x, x + dx], [y, y - dy], c="black")
            self.dibujar_arbol(nodo.derecho, x + dx, y - dy, dx / 2, dy, ax)

    def generar_grafico(self, tipo):
        """Genera la imagen del recorrido seleccionado"""
        if tipo == "preorden":
            recorrido = [f"({n.valor_x},{n.valor_y})" for n in self.arbol.preorden()]
        elif tipo == "inorden":
            recorrido = [f"({n.valor_x},{n.valor_y})" for n in self.arbol.inorden()]
        elif tipo == "postorden":
            recorrido = [f"({n.valor_x},{n.valor_y})" for n in self.arbol.postorden()]
        else:
            recorrido = [f"({n.valor_x},{n.valor_y})" for n in self.arbol.anchura()]

        # Preparar texto con salto de línea cada 80 caracteres
        recorrido_str = " -> ".join(recorrido)
        recorrido_wrapped = "\n".join(textwrap.wrap(recorrido_str, width=80))

        # Graficar con matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title(f"Recorrido {tipo.capitalize()}", fontsize=14, fontweight="bold")

        # Dibujar el árbol binario si existe
        if self.arbol.raiz:
            self.dibujar_arbol(self.arbol.raiz, 0, 0, 8, 3, ax)

        # Mostrar texto del recorrido debajo
        ax.text(-15, -12, recorrido_wrapped, fontsize=12, va="top", ha="left", wrap=True)

        # Ajustar límites del gráfico
        ax.axis("off")
        ax.set_xlim(-15, 15)
        ax.set_ylim(-15, 5)

        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        # Convertir a surface
        imagen = pygame.image.load(buf, "recorrido.png")
        self.img_surface = pygame.transform.scale(
            imagen,
            (self.config["ancho_pantalla"], self.config["alto_pantalla"] - 100)
        )

    def iniciar(self):
        print("Escena: Recorridos del árbol")

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                # volver al menú
                from game.views.menu import Menu
                fondo = pygame.image.load(self.config["fondos"]["menu"]).convert()
                fondo = pygame.transform.scale(
                    fondo,
                    (self.config["ancho_pantalla"], self.config["alto_pantalla"])
                )
                self.manager.cambiar_escena(Menu(self.manager, self.config, fondo))

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for clave, boton in self.botones.items():
                    if boton.rect.collidepoint(evento.pos):
                        self.recorrido_actual = clave
                        self.generar_grafico(clave)

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        if self.img_surface:
            pantalla.blit(self.img_surface, (0, 0))

        for boton in self.botones.values():
            boton.pantalla = pantalla
            boton.dibujar_en_pantalla()
