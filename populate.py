import numpy as np
from actor import Actor

def populate_rooms(blocking_tiles, blocking_entities, entities, rooms, empty_room_prob=0.5):
    monsters = _read_dgn_file('./entities/monsters.dgn')
    for room in rooms:
        if np.random.rand() > empty_room_prob:
            _place_entities(blocking_tiles, blocking_entities, entities, room, monsters)

def _place_entities(blocking_tiles, blocking_entities, entities, room, monsters):
    room_x, room_y, room_w, room_h = room
    if np.random.rand() < 0.5:
        name = 'skitterling'
    else:
        name = 'robot'
    blocked = True
    while blocked:
        x = np.random.randint(room_x, room_x + room_w)
        y = np.random.randint(room_y, room_y + room_h)
        coords = (x, y)
        if not blocking_entities[x, y]:
            blocked = False
        # could add condition to check for within-room walls (blocking tiles)
    monster = Actor(name, monsters[name]['symbol'], monsters[name]['blocks'], coords)
    blocking_entities[x, y] = 1
    entities.append(monster)

def _read_dgn_file(path):
    entities = {}
    with open(path) as dgn_file:
        for line in dgn_file:
            if line == '\n':
                entities[name] = attributes
            elif '>' in line:
                name = line.strip()[1:]
                attributes = {}
            else:
                att_name, att_value = line.strip().split(':')
                attributes[att_name] = att_value

    return entities
