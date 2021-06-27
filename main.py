from bearlibterminal import terminal as blt
from actor import Actor
from map_gen import Level

class Game:
    def __init__(self):
        blt.open()
        blt.set('window: size=80x40')

    def run(self):
        while blt.read() != blt.TK_Q:
            self.level.render(self.player)
            #blt.refresh()
        blt.close()

    def new_game(self):
        self.player = Actor(40, 20)
        self.level = Level(self.player)
        self.level.create_level(display=True)

a = Game()
a.new_game()
a.run()
