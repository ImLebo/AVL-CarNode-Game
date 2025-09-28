import pygame

class GestorColisiones:
    def __init__(self, arbol, carro, config, cola_eventos=None):
        self.arbol = arbol
        self.carro = carro
        self.config = config
        self.cola_eventos = cola_eventos  # para avisar al graficador

    def verificar(self, mundo_x):
        """
        Verifica colisiones del carro con obstáculos visibles
        y elimina los que ya fueron superados (x2 < mundo_x).
        Devuelve True si el carro se queda sin energía (Game Over).
        """
        carro_rect = self.carro.rect()

        # 🔎 Obtener todos los nodos del árbol
        todos = self.arbol.inorden()

        visibles = []
        obstaculos_a_eliminar = []

        for nodo in todos:
            # Obstáculo ya quedó atrás
            if nodo.x2 < mundo_x:
                obstaculos_a_eliminar.append(nodo)

            # Obstáculo en rango visible
            elif nodo.x1 <= mundo_x + self.config["ancho_pantalla"]:
                visibles.append(nodo)

        # ⚡ Verificar colisiones solo con visibles
        for nodo in visibles:
            x = nodo.x1 - mundo_x
            y = nodo.y1
            w = nodo.x2 - nodo.x1
            h = nodo.y2 - nodo.y1
            obstaculo_rect = pygame.Rect(x, y, w, h)

            if carro_rect.colliderect(obstaculo_rect):
                print(f"💥 Colisión con {nodo.tipo} en ({nodo.x1},{nodo.y1})")
                self.carro.energia -= 10

        # ⚡ Eliminar los ya pasados
        for nodo in obstaculos_a_eliminar:
            print(f"✔ Eliminando obstáculo {nodo.tipo} en ({nodo.x1},{nodo.y1})")
            self.arbol.eliminar(nodo)
            if self.cola_eventos:
                self.cola_eventos.put("actualizar")  # avisar al graficador

        return self.carro.energia <= 0
