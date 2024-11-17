from pico2d import*

import kirby_world
import kirby_game_framework
from kirby import Kirby
from kirby_background import Background_kirby
from ice_monster import Ice_Monster


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            kirby_game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            kirby_game_framework.quit()
        else:
            kirby.handle_event(event)

def init():
    global kirby
    global background
    global ice_monster

    kirby = Kirby()
    background = Background_kirby(kirby)
    ice_monster = Ice_Monster(background)

    kirby_world.add_object(background, 1)
    kirby_world.add_object(kirby,1)
    kirby_world.add_object(ice_monster, 1)

    kirby_world.add_collision_pair('kirby:map', kirby, None)
    kirby_world.add_collision_pair('kirby:map',None,background)
    kirby_world.add_collision_pair('kirby:ice',kirby,ice_monster)

def finish():
    kirby_world.clear()

def update():
    kirby_world.update()
    kirby_world.handle_collisions()
    pass

def draw():
    clear_canvas()
    kirby_world.render()
    update_canvas()


