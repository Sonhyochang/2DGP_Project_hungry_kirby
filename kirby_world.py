world = [[],[]]

def add_object(o,depth):
    world[depth].append(o)

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
            return

def clear():
    for layer in world:
        layer.clear()

def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True