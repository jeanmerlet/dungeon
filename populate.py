import numpy as np
from actor import Actor

def populate_rooms(entities, rooms, empty_room_prob=0.5):
    monsters = _read_dgn_file('./entities/monsters.dgn')
    for room in rooms:
        if np.random.rand() > empty_room_prob:
            _place_entities(entities, room, monsters)

def _place_entities(entities, room, monsters):
    room_x, room_y, room_w, room_h = room
    if np.random.rand() < 0.5:
        monster_name = 'skitterling'
    else:
        monster_name = 'robot'
    x = np.random.randint(room_x, room_x + room_w)
    y = np.random.randint(room_y, room_y + room_h)
    coords = (x, y)
    monster = Actor(monster_name, monsters[monster_name]['symbol'], coords)
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

    #print(entities)
    return entities
