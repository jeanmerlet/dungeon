from bearlibterminal import terminal as blt
from actor import Actor
from event_handler import EventHandler
import map_gen

class Game:
    def __init__(self):
        blt.open()
        blt.set('window: size=80x40')
        self.event_handler = EventHandler
        self.quit = False

    def run(self):
        while not self.quit:
            action = self.event_handler.read()
            self.update(action)
            self.level.render()
        blt.close()

    def new_game(self):
        self.player = Actor('player', '[color=amber]@', coords=[0, 0])
        self.entities = [self.player]
        self.level = map_gen.Level(self.entities)
        self.level.create_level()
        self.event_handler = EventHandler(cmd_domains=['movement', 'menu'])

    def update(self, action):
        if action:
            if 'move' in action:
                self.move_player(action['move'])
            elif 'quit' in action:
                self.quit = True
                
    def move_player(self, move):
        dx, dy = move
        end_x = self.player.x + dx
        end_y = self.player.y + dy
        if self.level.tiles[end_x, end_y] != 0:
            self.player.move(dx, dy)

a = Game()
a.new_game()
a.run()
