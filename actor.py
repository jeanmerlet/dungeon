class Actor:
    def __init__(self, name, symbol, coords, fov_id=None, fov_radius=None):
        self.name = name
        self.symbol = symbol
        self.x, self.y = coords
        self.fov_id = fov_id
        self.fov_radius = fov_radius

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
