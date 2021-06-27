from bearlibterminal import terminal as blt
import numpy as np
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
        
    def create_level(self, display=False):
        num_rooms = np.random.randint(6, 10)
        ellipse_xys = self.create_ellipse_xys()
        #if display: self.render(self.player)
        rooms = []
        while num_rooms > 0:
            room = self.create_room(ellipse_xys)
            num_rooms -= 1
            if display: self.render(self.player)
            #if i > 0: self.connect_room(room, rooms[-1])
            #if display: self.render(self.player)
        ellipse_xys = self.create_ellipse_xys(dig=True)
        if display: self.render(self.player)

    def create_ellipse_xys(self, dig=False):
        ellipse_xys = []
        d = ((self.width // 3))**2
        a = (self.height / self.width)**2
        for i in range(self.width):
            for j in range(self.height):
                x = i - self.width // 2
                y = j - self.height // 2
                dist = (x**2 + (y**2 // a))
                if dist < d and dist > d - 128:
                    ellipse_xys.append((i, j))
                    if dig:
                        self.tiles[i, j] = 1
        return ellipse_xys

    def create_room(self, ellipse_xys):
        # x, y are top left floor tile of (rectangular) rooms
        # w, h are the number of floor tiles across and down in the room
        x, y = ellipse_xys[np.random.randint(len(ellipse_xys))]
        x += np.random.randint(-4, 4)
        y += np.random.randint(-4, 4)
        w = np.random.randint(4, 10)
        h = np.random.randint(3, 8)
        if self.is_room_valid(x, y, w, h):
            self.tiles[x:x+w, y:y+h] = 1
        else:
            self.create_room(ellipse_xys)
        return [x, y, w, h]

    def is_room_valid(self, x, y, w, h):
        #if np.any(self.tiles[x-1:x+w+2, y-1:y+h+2]):
        if np.any(self.tiles[x-3:x+w+5, y-3:y+h+5]):
            return False
        elif x+w+2 >= self.width or y+h+2 >= self.height:
            return False
        return True

    def render(self, player):
        px = player.x
        py = player.y
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x, y] == 0:
                    blt.print(x, y, "[color=blue]#") 
                else:
                    blt.print(x, y, "[color=blue].")
        blt.print(px, py, "[color=red]@")
        blt.refresh()

    def connect_rooms(self, display):
        rooms_idx = np.arange(len(self.rooms))
        room1 = pick_room(rooms_idx)
        x1, y1 = pick_floor_in_room(room1)
        while len(rooms_idx) > 0:
            room2 = pick_room(rooms_idx)
            x2, y2 = pick_floor_in_room(room2)
            if np.random.rand() < 0.5:
                ew = 1 if np.random.rand() < 0.5 else -1
                ns = 0
            else:
                ew = 0
                ns = 1 if np.random.rand() < 0.5 else -1
            x, y = self.step_connect(x, y, ns, ew, display, on_floor=True)
            self.step_connect(x, y, ns, ew, display, on_floor=False)
            if display:
                self.render(self.player)

    def step_connect(self, x, y, ns, ew, display, on_floor):
        while True:
            x += ew
            y += ns
            if on_floor:
                if self.tiles[x, y] == 1:
                    continue
                else:
                    return x - ew, y - ns
            if not on_floor:
                if (x > 0 and x < self.width - 1 and
                    y > 0 and y < self.height - 1):
                    if self.tiles[x, y] == 0:
                        self.tiles[x, y] = 1
                        continue
            return
                
    def pick_floor_in_room(room):
        x, y, w, h = room
        x = np.random.randint(x, x+w)
        y = np.random.randint(y, y+h)
        return x, y

    def pick_room(self, rooms_idx):
        idx = np.random.randint(len(rooms_idx))
        np.delete(rooms_idx, idx)
        return self.rooms[idx]



