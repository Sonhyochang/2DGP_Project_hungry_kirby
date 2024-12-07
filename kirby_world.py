world = [[],[]]

collision_pairs ={}

def add_object(o,depth):
    world[depth].append(o)

def add_objects (ol, depth):
    world[depth] += ol

def render():
    for layer in world:
        for o in layer:
            o.draw()

def update():
    for layer in world:
        for o in layer:
            o.update()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return

def clear():
    for layer in world:
        layer.clear()

def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    # a_bb_list = a.get_bb()
    # b_bb_list = b.get_bb()
    #
    # for a in a_bb_list:
    #     left_a, bottom_a, right_a, top_a = a
    #     for b1,b2,b3,b4 in b_bb_list:
    #         print(f"Current b: {b1,b2,b3,b4}")
    #         left_b, bottom_b, right_b, top_b = [b1,b2,b3,b4]

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def add_collision_pair(group,a,b):
    if group not in collision_pairs:
        collision_pairs[group] = [[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a,b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)