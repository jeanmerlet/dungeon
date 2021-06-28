class Actor:
    def __init__(self, name, symbol, coords):
        self.name = name
        self.symbol = symbol
        self.x, self.y = coords

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
