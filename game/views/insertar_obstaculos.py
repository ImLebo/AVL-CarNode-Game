import pygame
import json
import os

CONFIG_FILE = os.path.join("config", "obstaculos.json")

class ObstaculoForm:
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config
        self.pantalla = manager.pantalla
        self.font = pygame.font.SysFont("consolas", 24)
        self.inputs = {
            "x1": "",
            "x2": "",
            "y1": "",
            "y2": "",
            "tipo": "",
            "img": ""
        }
        self.current_field = "x1"
        self.fields = list(self.inputs.keys())
        self.index = 0
    
    def iniciar(self):
        print("")
        
    def actualizar(self):
        pass

    def manejar_eventos(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:  # cambiar de campo
                    self.index = (self.index + 1) % len(self.fields)
                    self.current_field = self.fields[self.index]
                elif event.key == pygame.K_BACKSPACE:  # borrar
                    self.inputs[self.current_field] = self.inputs[self.current_field][:-1]
                elif event.key == pygame.K_RETURN:  # guardar en JSON
                    from game.views.menu import Menu
                    fondo = pygame.image.load(self.config["fondos"]["menu"]).convert()
                    fondo = pygame.transform.scale(
                        fondo,
                        (self.config["ancho_pantalla"], self.config["alto_pantalla"])
                    )
                    self.manager.cambiar_escena(Menu(self.manager, self.config, fondo))
                    self.save()
            else:
                if hasattr(event, "text"):
                    self.inputs[self.current_field] += event.text

    def dibujar(self, pantalla):
        pantalla.fill((30, 30, 30))
        y = 100
        for i, (campo, valor) in enumerate(self.inputs.items()):
            color = (0, 255, 0) if campo == self.current_field else (200, 200, 200)
            text = self.font.render(f"{campo}: {valor}", True, color)
            pantalla.blit(text, (100, y))
            y += 50

        hint = self.font.render("TAB: cambiar campo | ENTER: guardar", True, (180, 180, 180))
        pantalla.blit(hint, (100, y + 20))

    def save(self):
        data = []
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        data.append({
            "x1": int(self.inputs["x1"]),
            "x2": int(self.inputs["x2"]),
            "y1": int(self.inputs["y1"]),
            "y2": int(self.inputs["y2"]),
            "tipo": int(self.inputs["tipo"]),
            "img": self.inputs["img"]
        })
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("✅ Obstáculo guardado en obstaculos.json")
