from bearlibterminal import terminal as blt
import numpy as np

from actor import Actor
from event_handler import EventHandler
import map_gen
from display import Display
from fov import FieldOfView
import populate

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
        self.player = Actor('player', '[color=amber]@', blocks=True, coords=[0, 0],
                            health=10, attack=3, defense=3, fov_id=0, fov_radius=8)
        self.blocking_entities = np.zeros((self.width, self.height), dtype=int)
        self.entities = [self.player]
        self.level = map_gen.Level(width=self.width, height=self.height)
        self.level.create_level(self.entities, display=True)
        populate.populate_rooms(self.level.blocking_tiles, self.blocking_entities,
                                self.entities, self.level.rooms)
        self._place_player()
        self.fov = FieldOfView(self.level.opaque_tiles, self.level.explored_tiles,
                               self.width, self.height)
        self.fov.do_fov(self.player)
        self.display = Display(self.player, self.entities, self.level.blocking_tiles,
                               self.level.explored_tiles, self.width, self.height, self.fov.fov_id)
        self.event_handler = EventHandler(cmd_domains=['movement', 'menu'])

    def _update(self, action):
        if action:
            if 'move' in action:
                self._move_player(action['move'])
            elif 'quit' in action:
                self.quit = True
            self.fov.do_fov(self.player)

    def _place_player(self):
        x = np.random.randint(self.level.width)
        y = np.random.randint(self.level.height)
        if self.level.blocking_tiles[x, y] or self.blocking_entities[x, y]:
            self._place_player()
        else:
            self.player.x, self.player.y = x, y
            self.blocking_entities[x, y] = 1
                
    def _move_player(self, move):
        dx, dy = move
        x, y = self.player.x, self.player.y
        end_x, end_y = x + dx, y + dy
        if not self.level.blocking_tiles[end_x, end_y]:
            if not self.blocking_entities[end_x, end_y]:
                self.player.move(dx, dy)
                self.blocking_entities[x, y] = 0
                self.blocking_entities[end_x, end_y] = 1
            elif self.blocking_entities[end_x, end_y]:
                entity = [e for e in self.entities if e.x == end_x and e.y == end_y][0]
                #self.player.attack(entity.defense)
                print(f'blocking entity {entity.name} here')

# 1960
a = Game(7536)
a.new_game()
a.run()
