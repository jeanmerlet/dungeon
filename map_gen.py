from bearlibterminal import terminal as blt
import numpy as np
import shapes
import time

class Level:
    """
    0: wall
    1: floor
    """

    def __init__(self, player, width=80, height=40):
        self.player = player
        self.width = width
        self.height = height
        self.tiles = np.zeros((width, height), dtype=np.int32)

    def render(self, player):
        px = player.x
        py = player.y
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x, y]
                if tile == 0:
                    blt.print(x, y, "[color=blue]#") 
                elif tile == 1:
                    blt.print(x, y, "[color=blue].")
                elif tile == 2:
                    blt.print(x, y, "[color=green].")
                elif tile == 3:
                    blt.print(x, y, "[color=red].")
        blt.print(px, py, "[color=red]@")
        blt.refresh()
        
    def create_level(self, display=False):
        radius = self.width / 4
        y_scaling = self.height / self.width
        main_loop = self.get_loop_xys(radius, y_scaling, display=False, fill=False)
        rooms = self.create_rooms(main_loop, display)
        self.connect_rooms(rooms, display)

    def get_loop_xys(self, r, s, display, fill):
        coords = []
        pi_range = np.linspace(0, 2*np.pi, 1000)
        for i, t in enumerate(pi_range):
            x = round(r * np.cos(t) + self.width // 2)
            y = round(r * s * np.sin(t) + self.height // 2)
            if i == 0:
                coords.append((x, y))
            elif i > 0 and (x, y) != coords[-1]:
                coords.append((x, y))
                if fill: self.tiles[x, y] = 1
                if display: self.render(self.player)
        return coords

    def create_rooms(self, coords, display):
        num_coords = len(coords)
        scale = 10
        rooms = []
        for i in range(num_coords // scale):
            x, y = coords[np.random.randint(i*scale - 2, i*scale + 2)]
            room = self.create_room(x, y)
            if room:
                rooms.append(room)
                if display: 
                    self.render(self.player)
        rooms.append(rooms[0])
        return rooms

    def create_room(self, x, y):
        # new_x, new_y are top left floor tile of (rectangular) rooms
        # w, h are the number of floor tiles across and down in the room
        tries_remaining = 10
        while tries_remaining > 0:
            w = np.random.randint(4, 10)
            h = np.random.randint(3, 8)
            if self.is_room_valid(x, y, w, h):
                self.tiles[x:x+w, y:y+h] = 1
                return [x, y, w, h]
            else:
                tries_remaining -= 1
        return None

    def is_room_valid(self, x, y, w, h):
        if np.any(self.tiles[x-3:x+w+5, y-3:y+h+5]):
            return False
        elif x+w+2 >= self.width or y+h+2 >= self.height:
            return False
        return True

    def connect_rooms(self, rooms, display):
        for i in range(len(rooms) - 1):
            x1, y1, w1, h1 = rooms[i]
            x2, y2, w2, h2 = rooms[i+1]
            start = (x1 + np.random.randint(w1),
                     y1 + np.random.randint(h1))
            end = (x2 + np.random.randint(w2),
                   y2 + np.random.randint(h2))
            if start[0] < end[0]:
                if start[1] < end[1]:
                    self.tiles[end[0], start[1]:end[1] + 1] = 1
                    self.tiles[start[0]:end[0], start[1]] = 1
                else:
                    self.tiles[start[0], end[1]:start[1]] = 1
                    self.tiles[start[0]:end[0], end[1]] = 1
            else: 
                if start[1] < end[1]:
                    self.tiles[start[0], start[1]:end[1] + 1] = 1
                    self.tiles[end[0]:start[0], end[1]] = 1
                else:
                    self.tiles[end[0], end[1]:start[1]] = 1
                    self.tiles[end[0]:start[0], start[1]] = 1
            if display: 
                self.render(self.player)

