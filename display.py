from bearlibterminal import terminal as blt
import numpy as np

class Display:
    def __init__(self, player, entities, blocking_tiles, explored_tiles,
                 width, height, fov_id):
        self.player = player
        self.entities = entities
        self.blocking_tiles = blocking_tiles
        self.explored_tiles = explored_tiles
        self.width, self.height = width, height
        self.fov_id = fov_id

    def render(self):
        blt.clear()
        for x in range(self.width):
            for y in range(self.height):
                tile = self.blocking_tiles[x, y]
                if self.explored_tiles[x, y]:
                #if True:
                    if self.fov_id[x, y] == self.player.fov_id:
                    #if True:
                        if not tile:
                            blt.print(x, y, "[color=220,220,150].")
                        else:
                            blt.print(x, y, "[color=70,70,90]#")
                    else:
                        if not tile:
                            blt.print(x, y, "[color=40,40,40].")
                        else:
                            blt.print(x, y, "[color=40,40,40]#")

        for entity in self.entities:
            x, y = entity.x, entity.y
            if self.fov_id[x, y] == self.player.fov_id:
            #if True:
                blt.print(entity.x, entity.y, entity.symbol)
        blt.refresh()

class Viewport:
    def __init__(self, entities, level):
        self.entities = entities
        self.tiles = level.tiles
        self.width, self.height = level.width, level.height

