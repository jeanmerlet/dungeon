import numpy as np

class FieldOfView:
    # MULTipliers for transforming coordinates to other octants
    MULT = np.array([[1,  0,  0, -1, -1,  0,  0,  1],
                     [0,  1, -1,  0,  0, -1,  1,  0],
                     [0,  1,  1,  0,  0, -1, -1,  0],
                     [1,  0,  0,  1, -1,  0,  0, -1]], dtype=np.float32)

    def do_fov(self, level, origin):
        tiles = level.tiles
        x, y = origin.x, origin.y
        fov_id, radius = origin.fov_id, origin.fov_r# + 0.5
        #radius = radius**2
        #self.light(level, fov_id, x, y)
        for octant in range(8):
            self.cast_light(level, fov_id, x, y, radius, 1, 1.0, 0.0,
                            self.MULT[0, octant], self.MULT[1, octant],
                            self.MULT[2, octant], self.MULT[3, octant])
            break

    def _cast_light(self, tiles, fov_id, x, y, radius, row, start, end, xx, xy, yx, yy):
        for i in range(row, radius+1):
            X = 
