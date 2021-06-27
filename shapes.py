import numpy as np

def ellipse(x, y, w, h, fill=True):
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

