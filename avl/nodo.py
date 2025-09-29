class Obstaculo: 
    def __init__(self, x1=0, x2=0, y1=0, y2=0, tipo="", img=None):
        
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1 
        self.y2 = y2
        self.tipo = tipo
        self.img = img
        self.img_surface = None
        self.colisionado = False

class Nodo(Obstaculo):
    def __init__(self, padre=None, x1=0, x2=0, y1=0, y2=0, tipo="", img=None):
        # Propiedades de obstaculo
        super().__init__(x1, x2, y1, y2, tipo, img)
        
        # Caracteristicas de AVL
        self.valor_x = x1
        self.valor_y = y1
        self.factor_balanceo = 0
        self.izquierdo = None
        self.derecho = None
        self.padre = padre