from bearlibterminal import terminal as blt

class Display:
    def __init__(self, entities, level):
        self.entities = entities
        self.tiles = level.tiles
        self.width, self.height = level.width, level.height

    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                if tile.blocked:
                    blt.print(x, y, "[color=70,70,90]#")
                else:
                    blt.print(x, y, "[color=220,220,150].")

        for entity in self.entities:
            blt.print(entity.x, entity.y, entity.symbol)
        blt.refresh()

class Viewport:
    def __init__(self, entities, level):
        self.entities = entities
        self.tiles = level.tiles
        self.width, self.height = level.width, level.height

