# GameEngine.py

class GameEngine:
    def __init__(self):
        self.characters = {}  # Mapeia nomes de personagens para seus atributos
        self.scene = None

    def create_character(self, name, sprite_file, x, y):
        if name in self.characters:
            print(f"GameEngine: Personagem '{name}' já existe.")
        else:
            self.characters[name] = {
                'sprite': sprite_file,
                'x': x,
                'y': y
            }
            print(f"GameEngine: Personagem '{name}' criado em ({x}, {y}).")

    def move_character(self, name, direction, distance):
        if name in self.characters:
            char = self.characters[name]
            if direction == 'UP':
                char['y'] -= distance
            elif direction == 'DOWN':
                char['y'] += distance
            elif direction == 'LEFT':
                char['x'] -= distance
            elif direction == 'RIGHT':
                char['x'] += distance
            print(f"GameEngine: Personagem '{name}' movido para ({char['x']}, {char['y']}).")
        else:
            print(f"GameEngine: Personagem '{name}' não encontrado.")

    def set_character_position(self, name, x, y):
        if name in self.characters:
            self.characters[name]['x'] = x
            self.characters[name]['y'] = y
            print(f"GameEngine: Posição de '{name}' definida para ({x}, {y}).")
        else:
            print(f"GameEngine: Personagem '{name}' não encontrado.")

    # Implement other methods as needed
