import numpy as np

class FieldOfView:
    # multipliers for transforming coordinates to other octants
    MULT = np.array([[1,  0,  0,  1, -1,  0,  0, -1],
                     [0,  1,  1,  0,  0, -1, -1,  0],
                     [0,  1, -1,  0,  0, -1,  1,  0],
                     [1,  0,  0, -1, -1,  0,  0,  1]], dtype=np.int32)

    def __init__(self, opaque_tiles, explored_tiles, width, height):
        self.opaque_tiles = opaque_tiles
        self.explored_tiles = explored_tiles
        self.fov_id = np.zeros((width, height), dtype=np.int32)

    def do_fov(self, origin):
        origin.fov_id += 1
        x, y = origin.x, origin.y
        self._light(origin.fov_id, x, y)
        radius = origin.fov_radius
        for octant in range(8):
            self._cast_light(origin.fov_id, x, y, radius, 1, 1.0, 0.0,
                             self.MULT[0, octant], self.MULT[1, octant],
                             self.MULT[2, octant], self.MULT[3, octant])

    def _cast_light(self, o_fov_id, ox, oy, radius, row, start, end, xx, xy, yx, yy):
        if start < end:
            return

        radius_sq = radius**2
        for j in range(row, radius+1):
            blocked = False
            dx = -j - 1
            dy = -j
            while dx <= 0:
                dx += 1
                X = ox + dx * xx + dy * xy
                Y = oy + dx * yx + dy * yy
                l_slope = (dx - 0.5)/(dy + 0.5)
                r_slope = (dx + 0.5)/(dy - 0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    if dx**2 + dy**2 < radius_sq:
                        self._light(o_fov_id, X, Y)
                    if blocked:
                        if self.opaque_tiles[X, Y]:
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.opaque_tiles[X, Y] and j < radius:
                            blocked = True
                            self._cast_light(o_fov_id, ox, oy, radius, j+1,
                                             start, l_slope, xx, xy, yx, yy)
                            new_start = r_slope
            if blocked:
                break

    def _light(self, origin_fov_id, x, y):
        self.explored_tiles[x, y] = True
        self.fov_id[x, y] = origin_fov_id
