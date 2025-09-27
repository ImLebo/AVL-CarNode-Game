import pygame
import sys
import json
from avl.nodo import Nodo
from avl.arbol_avl import ArbolAVL
from models.carro import Carro

# ---------------------------------------------------
# CONFIGURACIÓN (simulada - luego cargaremos de JSON)
# ---------------------------------------------------
CONFIG = {
    "ancho_pantalla": 800,
    "alto_pantalla": 600,
    "color_fondo": (135, 206, 235),  # azul cielo
    "carro_color": (255, 200, 0),
    "carro_ancho": 50,
    "carro_alto": 30,
    "velocidad_y": 5,
    "avance_px": 5,           # avance del mundo (x)
    "intervalo_ms": 200,      # cada cuánto avanza
    "salto_altura": 100
}

# ---------------------------------------------------
# CLASE CARRO
# ---------------------------------------------------

# ---------------------------------------------------
# FUNCIÓN PRINCIPAL
# ---------------------------------------------------
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((CONFIG["ancho_pantalla"], CONFIG["alto_pantalla"]))
    pygame.display.set_caption("Juego con Árbol AVL")

    reloj = pygame.time.Clock()

    # Crear carro
    carro = Carro('../config/carro.json')

    # Crear árbol AVL de obstáculos
    arbol = ArbolAVL()
    arbol.insertar(Nodo(x1=300, y1=450, x2=350, y2=480, tipo="roca"))
    arbol.insertar(Nodo(x1=500, y1=420, x2=540, y2=460, tipo="pincho"))
    arbol.insertar(Nodo(x1=700, y1=400, x2=760, y2=440, tipo="hueco"))

    # Posición del mundo (simulación de avance horizontal)
    mundo_x = 0
    tiempo_avance = pygame.USEREVENT + 1
    pygame.time.set_timer(tiempo_avance, CONFIG["intervalo_ms"])

    energia = 100

    # Loop principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == tiempo_avance:
                mundo_x += CONFIG["avance_px"]

        teclas = pygame.key.get_pressed()
        carro.mover(teclas)
        carro.actualizar(CONFIG["alto_pantalla"])

        # Dibujar fondo
        pantalla.fill(CONFIG["color_fondo"])

        # Dibujar carro
        carro.dibujar(pantalla)

        # Dibujar obstáculos visibles
        visibles = arbol.inorden()  # más adelante usaremos consulta por rango
        for nodo in visibles:
            # Convertir coordenadas del mundo a pantalla
            x1 = nodo.x1 - mundo_x
            y1 = nodo.y1
            ancho = nodo.x2 - nodo.x1
            alto = nodo.y2 - nodo.y1
            rect_obs = pygame.Rect(x1, y1, ancho, alto)

            pygame.draw.rect(pantalla, (100, 100, 100), rect_obs)

            # Colisión
            if carro.rect().colliderect(rect_obs):
                energia -= nodo.danio if hasattr(nodo, "danio") else 5
                print(f"¡Colisión con {nodo.tipo}! Energía: {energia}")

        # Dibujar energía
        fuente = pygame.font.SysFont(None, 30)
        texto = fuente.render(f"Energía: {energia}%", True, (0, 0, 0))
        pantalla.blit(texto, (10, 10))

        pygame.display.flip()
        reloj.tick(60)

# ---------------------------------------------------
if __name__ == "__main__":
    main()
