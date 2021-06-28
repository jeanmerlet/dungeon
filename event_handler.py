from bearlibterminal import terminal as blt

class EventHandler:
    def __init__(self, cmd_domains):
        self.cmd_domains = cmd_domains

    def read(self):
        if blt.has_input():
            return self.handle_event(blt.read())

    def handle_event(self, event):
        action = {}
        for cmd_domain in self.cmd_domains:
            if cmd_domain == 'movement':
                if event == blt.TK_KP_8:
                    action['move'] = [0, -1]
                elif event == blt.TK_KP_2:
                    action['move'] = [0, 1]
                elif event == blt.TK_KP_4:
                    action['move'] = [-1, 0]
                elif event == blt.TK_KP_6:
                    action['move'] = [1, 0]
                elif event == blt.TK_KP_7:
                    action['move'] = [-1, -1]
                elif event == blt.TK_KP_9:
                    action['move'] = [1, -1]
                elif event == blt.TK_KP_3:
                    action['move'] = [1, 1]
                elif event == blt.TK_KP_1:
                    action['move'] = [-1, 1]
                elif event == blt.TK_KP_5:
                    action['move'] = [0, 0]
            elif cmd_domain == 'menu':
                if event == blt.TK_Q:
                    action['quit'] = True

        return action
