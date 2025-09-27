from obstaculo import Obstaculo

class Nodo(Obstaculo):
    def __init__(self, valor, padre=None, x1=0, x2=0, y1=0, y2=0, tipo="", img=None):
        # Propiedades de obstaculo
        super().__init__(x1, x2, y1, y2, tipo, img)
        
        # Caracteristicas de AVL
        self.valor_x = x1
        self.valor_y = y1
        self.factor_balanceo = 0
        self.izquierdo = None
        self.derecho = None
        self.padre = padre