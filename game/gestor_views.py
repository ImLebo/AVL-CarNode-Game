class GestorViews:
    def __init__(self, pantalla, config):
        self.escena_actual = None
        self.pantalla = pantalla 
        self.config = config

    def cambiar_escena(self, nueva_escena):
        """ Cambia a una nueva escena """
        self.escena_actual = nueva_escena
        self.escena_actual.iniciar()

    def manejar_eventos(self, eventos):
        if self.escena_actual:
            self.escena_actual.manejar_eventos(eventos)

    def actualizar(self):
        if self.escena_actual:
            self.escena_actual.actualizar()

    def dibujar(self, pantalla):
        if self.escena_actual:
            self.escena_actual.dibujar(pantalla)
    