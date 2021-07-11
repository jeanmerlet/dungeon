from bearlibterminal import terminal as blt
import numpy as np

from actor import Actor
from event_handler import EventHandler
import map_gen
from display import Display
from fov import FieldOfView

class Game:
    def __init__(self, seed=None):
        blt.open()
        self.width, self.height = 80, 40
        blt.set(f'window: size={self.width}x{self.height}')
        self.event_handler = EventHandler
        self.quit = False
        if not seed:
            seed = np.random.randint(10000)
        np.random.seed(seed)
        print(f'seed: {seed}')

    def run(self):
        while not self.quit:
            action = self.event_handler.read()
            self._update(action)
            self.display.render()
        blt.close()

    def new_game(self):
        self.player = Actor('player', '[color=amber]@', coords=[0, 0], fov_id=0, fov_radius=8)
        self.entities = [self.player]
        self.level = map_gen.Level(width=self.width, height=self.height)
        self.level.create_level(self.entities, display=True)
        self._place_player()
        self.fov = FieldOfView(self.level.tiles, self.width, self.height)
        self.fov.do_fov(self.player)
        self.display = Display(self.player, self.entities, self.level, self.fov.fov_id)
        self.event_handler = EventHandler(cmd_domains=['movement', 'menu'])

    def _update(self, action):
        if action:
            if 'move' in action:
                self._move_player(action['move'])
            elif 'quit' in action:
                self.quit = True
            self.fov.do_fov(self.player)

    def _place_player(self):
        self.player.x = np.random.randint(self.level.width)
        self.player.y = np.random.randint(self.level.height)
        if self.level.tiles[self.player.x][self.player.y].blocked: self._place_player()
                
    def _move_player(self, move):
        dx, dy = move
        end_x = self.player.x + dx
        end_y = self.player.y + dy
        if not self.level.tiles[end_x][end_y].blocked:
            self.player.move(dx, dy)

a = Game(1960)
a.new_game()
a.run()
