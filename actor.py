class Attack:
    def __init__(self, name, damage):
        self.name = name
        self.dam = dam

class Defense:
    def __init__(self, name, defense):
        self.name = name
        self.value = defense

class Actor:
    def __init__(self, name, symbol, blocks, coords, health, attack, defense,
                 fov_id=None, fov_radius=None):
        self.name = name
        self.symbol = symbol
        self.blocks = blocks
        self.x, self.y = coords
        self.health = health
        self.attack = attack
        self.defense = defense
        self.fov_id = fov_id
        self.fov_radius = fov_radius

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def attack(self, target):
        
