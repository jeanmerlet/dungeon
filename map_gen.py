from bearlibterminal import terminal as blt
import numpy as np
import shapes
import time

class Tile:
    def __init__(self, blocked=True, transparent=False):
        self.blocked = blocked
        self.transparent = transparent
        self.explored = False

class Level:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.tiles = [[Tile() for j in range(height)] for i in range(width)]

    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                if tile.blocked:
                    blt.print(x, y, "[color=70,70,90]#") 
                else:
                    blt.print(x, y, "[color=220,220,150].")

        blt.refresh()
        
    def create_level(self, display=False):
        if display: blt.refresh()
        radius = self.width / 4
        y_scaling = self.height / self.width
        main_loop = self._get_loop_xys(radius, y_scaling, display=False, dig=False)
        rooms = self._create_rooms(main_loop, display)
        self._connect_rooms(rooms, display)
        self.render()

    def _get_loop_xys(self, r, s, display, dig):
        coords = []
        pi_range = np.linspace(0, 2*np.pi, 1000)
        for i, t in enumerate(pi_range):
            x = round(r * np.cos(t) + self.width // 2)
            y = round(r * s * np.sin(t) + self.height // 2)
            if i == 0:
                coords.append((x, y))
            elif i > 0 and (x, y) != coords[-1]:
                coords.append((x, y))
                if dig:
                    self.tiles[x][y].blocked = False
                    self.tiles[x][y].transparent = True
                if display: self.render()
        return coords

    def _create_rooms(self, coords, display):
        num_coords = len(coords)
        scale = 5
        rooms = []
        for i in range(num_coords // scale):
            x, y = coords[np.random.randint(i*scale - 2, i*scale + 2)]
            room = self._create_room(x, y)
            if room:
                rooms.append(room)
                if display: 
                    self.render()
        rooms.append(rooms[0])
        return rooms

    def _create_room(self, x, y):
        # new_x, new_y are top left floor tile of (rectangular) rooms
        # w, h are the number of floor tiles across and down in the room
        tries_remaining = 10
        while tries_remaining > 0:
            w = np.random.randint(4, 10)
            h = np.random.randint(3, 8)
            if self._is_room_valid(x, y, w, h):
                for i in range(x, x+w):
                    for j in range(y, y+h):
                        self.tiles[i][j].blocked = False
                        self.tiles[i][j].transparent = True
                return [x, y, w, h]
            else:
                tries_remaining -= 1
        return None

    def _is_room_valid(self, x, y, w, h):
        for i in range(x-3, x+w+5):
            for j in range(y-3, y+h+5):
                if i >= self.width or j >= self.height:
                    return False
                elif not self.tiles[i][j].blocked:
                    return False
        return True

    def _connect_rooms(self, rooms, display):
        for i in range(len(rooms) - 1):
            x1, y1, w1, h1 = rooms[i]
            x2, y2, w2, h2 = rooms[i+1]
            start = (x1 + np.random.randint(w1),
                     y1 + np.random.randint(h1))
            end = (x2 + np.random.randint(w2),
                   y2 + np.random.randint(h2))
            if start[0] < end[0]:
                if start[1] < end[1]:
                    for j in range(start[1], end[1] + 1):
                        self.tiles[end[0]][j].blocked = False
                        self.tiles[end[0]][j].transparent = True
                    for i in range(start[0], end[0]):
                        self.tiles[i][start[1]].blocked = False
                        self.tiles[i][start[1]].transparent = True
                else:
                    for j in range(end[1], start[1] + 1):
                        self.tiles[start[0]][j].blocked = False
                        self.tiles[start[0]][j].transparent = True
                    for i in range(start[0], end[0]):
                        self.tiles[i][end[1]].blocked = False
                        self.tiles[i][end[1]].transparent = True
            else: 
                if start[1] < end[1]:
                    for j in range(start[1], end[1] + 1):
                        self.tiles[start[0]][j].blocked = False
                        self.tiles[start[0]][j].transparent = True
                    for i in range(end[0], start[0]):
                        self.tiles[i][end[1]].blocked = False
                        self.tiles[i][end[1]].transparent = True
                else:
                    for j in range(end[1], start[1] + 1):
                        self.tiles[end[0]][j].blocked = False
                        self.tiles[end[0]][j].transparent = True
                    for i in range(end[0], start[0]):
                        self.tiles[i][start[1]].blocked = False
                        self.tiles[i][start[1]].transparent = True
            if display: 
                self.render()
