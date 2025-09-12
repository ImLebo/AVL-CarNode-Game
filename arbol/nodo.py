class Nodo:
    def __init__(self, valor, padre=None):
        self.valor = valor
        self.factor_balanceo = 0
        self.izquierdo = None
        self.derecho = None
        self.padre = padre