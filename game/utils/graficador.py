import threading, queue
import matplotlib.pyplot as plt
import pygame
from io import BytesIO

class GraficadorAVL(threading.Thread):
    def __init__(self, arbol, cola_eventos):
        super().__init__()
        self.arbol = arbol  # referencia al árbol AVL
        self.cola_eventos = cola_eventos
        self.running = True
        self.surface = None

    def run(self):
        plt.switch_backend("Agg")  # backend sin ventana
        while self.running:
            try:
                evento = self.cola_eventos.get(timeout=0.1)
                if evento == "actualizar":
                    self.dibujar_arbol()
            except queue.Empty:
                pass

    def dibujar_arbol(self):
        plt.clf()
        if not self.arbol.raiz:
            return

        posiciones = {}
        self._calcular_posiciones(self.arbol.raiz, 0, 0, posiciones)

        # Dibujar conexiones
        for nodo, (x, y) in posiciones.items():
            if nodo.izquierdo:
                xi, yi = posiciones[nodo.izquierdo]
                plt.plot([x, xi], [y, yi], "k-")
            if nodo.derecho:
                xd, yd = posiciones[nodo.derecho]
                plt.plot([x, xd], [y, yd], "k-")

        # Dibujar nodos
        for nodo, (x, y) in posiciones.items():
            plt.scatter(x, y, s=800, c="skyblue", edgecolors="black", zorder=3)
            plt.text(x, y, f"({nodo.valor_x},{nodo.valor_y})",
                    ha="center", va="center", fontsize=8, weight="bold")

        plt.axis("off")
        plt.tight_layout()

        # Guardar en buffer y convertir a Surface de pygame
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img = pygame.image.load(buf, "arbol.png")
        self.surface = img.convert_alpha()
        buf.close()
        
            
        # 🔧 Escalar aquí (ej: 250x200)
        self.surface = pygame.transform.smoothscale(img, (250, 200))

    def _calcular_posiciones(self, nodo, x, y, posiciones, dx=5, dy=-5, nivel=0):
        """
        Posiciona recursivamente los nodos en el plano
        x: posición horizontal (según subárbol)
        y: profundidad (nivel del árbol)
        """
        if nodo is None:
            return x

        # recorrer izquierda
        x = self._calcular_posiciones(nodo.izquierdo, x, y+dy, posiciones, dx, dy, nivel+1)

        # asignar posición actual
        posiciones[nodo] = (x, y)

        # recorrer derecha
        x = self._calcular_posiciones(nodo.derecho, x+dx, y+dy, posiciones, dx, dy, nivel+1)

        return x

    def detener(self):
        self.running = False
