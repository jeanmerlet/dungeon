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
        blt.refresh()
        self.width, self.height = width, height
        self.center_x = width // 2
        self.center_y = height // 2
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
        ## main loop ##
        radius = self.width / 5
        y_scaling = self.height / self.width
        main_loop = self._get_loop_xys(self.center_x, self.center_y, radius,
                                       y_scaling, display=False, dig=False)
        rooms = self._create_rooms(main_loop, display)
        self._connect_rooms(rooms, display, connect_last=True)
        ## side loops ##
        radius = self.width / 7
        num_rooms = len(rooms)
        loop_diff = -len(rooms) + 1
        anchor_indices = np.arange(num_rooms)
        for i in range(np.random.randint(3) + 1):
            anchor_rooms = []
            to_remove = []
            anchor_idx_a = np.random.choice(anchor_indices)
            anchor_idx_b = anchor_indices[(np.nonzero(anchor_indices == anchor_idx_a)[0][0] + 1) % num_rooms]
            anchor_rooms.append(rooms[anchor_idx_a])
            anchor_rooms.append(rooms[anchor_idx_b])
            to_remove.append(anchor_idx_a)
            to_remove.append(anchor_idx_b)
            diff = anchor_idx_b - anchor_idx_a
            if diff != 1 and diff != loop_diff : continue
            anchor_indices = anchor_indices[np.in1d(anchor_indices, to_remove, invert=True)]
            num_rooms = len(anchor_indices)
            side_loop_cx, side_loop_cy = self._get_side_loop_center(anchor_rooms, radius, y_scaling)
            #blt.print(side_loop_cx, side_loop_cy, "[color=red]*")
            #blt.refresh()
            #time.sleep(1)
            x1, y1, w1, h1 = anchor_rooms[0]
            cx1, cy1 = x1 + w1/2, y1 + h1/2
            anchor_center_slope = (side_loop_cy - cy1) / (side_loop_cx - cx1)
            rotation = np.arctan(anchor_center_slope)
            if side_loop_cx > self.center_x:
                rotation += np.pi
            side_loop = self._get_loop_xys(side_loop_cx, side_loop_cy, radius, y_scaling,
                                           display=False, dig=False, rotation=rotation)
                                           #display=True, dig=True, rotation=rotation)
            side_rooms = self._create_rooms(side_loop, display)
            for room in side_rooms:
                rooms.append(room)
            side_rooms = [anchor_rooms[0]] + side_rooms + [anchor_rooms[-1]]
            self._connect_rooms(side_rooms, display, connect_last=False)
            time.sleep(0.5)

    def _get_loop_xys(self, cx, cy, r, s, display, dig, rotation=0):
        dx = self.center_x - cx
        dy = self.center_y - cy
        coords = []
        pi_range = np.linspace(0, 2*np.pi, 1000)
        for i, t in enumerate(pi_range):
            x = round(r * np.cos(t + rotation) + self.width // 2) - dx
            y = round(r * s * np.sin(t + rotation) + self.height // 2) - dy
            if i == 0:
                coords.append((x, y))
            elif i > 0 and (x, y) != coords[-1]:
                coords.append((x, y))
                if dig:
                    self.tiles[x][y].blocked = False
                    self.tiles[x][y].transparent = True
                if display: self.render()
        return coords

    def _get_side_loop_center(self, rooms, radius, y_scaling):
        x1, y1, w1, h1 = rooms[0]
        x2, y2, w2, h2 = rooms[1]
        cx1, cy1 = x1 + w1/2, y1 + h1/2
        cx2, cy2 = x2 + w2/2, y2 + h2/2
        midx, midy = (cx1 + cx2)/2, (cy1 + cy2)/2
        #blt.print(round(cx1), round(cy1), "[color=red]1") 
        #blt.print(round(cx2), round(cy2), "[color=red]2") 
        #blt.print(round(midx), round(midy), "[color=red]M") 
        #blt.refresh()
        # ellipse centered at midpoint
        bi_ellipse_coords = self._get_loop_xys(round(midx), round(midy), radius,
                                               y_scaling, display=False, dig=False)
        max_dist = 0
        for coord in bi_ellipse_coords:
            x, y = coord
            dist = y_scaling * (x - self.center_x)**2 + (y - self.center_y)**2
            if dist > max_dist:
                max_dist = dist
                center = coord

        return center

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
                    #time.sleep(0.1)
        if len(rooms) > 0:
            return rooms
        else:
            return self._create_rooms(coords, display)

    def _create_room(self, x, y):
        # new_x, new_y are top left floor tile of (rectangular) rooms
        # w, h are the number of floor tiles across and down in the room
        tries_remaining = 10
        while tries_remaining > 0:
            w = np.random.randint(4, 10)
            h = np.random.randint(3, 8)
            cx = x - w // 2
            cy = y - h // 2
            if self._is_room_valid(cx, cy, w, h):
                for i in range(cx, cx+w):
                    for j in range(cy, cy+h):
                        self.tiles[i][j].blocked = False
                        self.tiles[i][j].transparent = True
                return [cx, cy, w, h]
            else:
                tries_remaining -= 1
        return None

    def _is_room_valid(self, x, y, w, h):
        for i in range(x-3, x+w+3):
            for j in range(y-3, y+h+3):
                if not (0 < i < self.width and 0 < j < self.height):
                    return False
                elif not self.tiles[i][j].blocked:
                    return False
        return True

    def _connect_rooms(self, rooms, display, connect_last):
        if connect_last:
            rooms.append(rooms[0])
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
                #time.sleep(0.2)
        if connect_last:
            rooms.pop()
