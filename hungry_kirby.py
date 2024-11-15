

from pico2d import*

import kirby_world
from kirby import Kirby

from kirby_background import Background_kirby

Back_WIDTH, Back_HEIGHT = 1024, 768

def handle_events():
    global running
    global dir
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        #elif event.type == SDL_KEYDOWN and SDLK_ESCAPE:
            #running = False
        else:
            kirby.handle_event(event)

def reset_world():
    global running
    global kirby
    global world
    global background
    global stage1


    running = True
    kirby = Kirby()
    background = Background_kirby(kirby)

    kirby_world.add_object(background, 1)
    kirby_world.add_object(kirby,1)

def update_world():
    kirby_world.update()
    pass

def render_world():
    clear_canvas()
    kirby_world.render()
    update_canvas()

open_canvas(Back_WIDTH,Back_HEIGHT)
reset_world()
# game loop

while running:
    handle_events()
    update_world()
    render_world()

    delay(0.05)
# finalization code
close_canvas()
