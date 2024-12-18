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
    global boss_map
    global boss
    global boss_die_time

    kirby = Kirby()
    background = Background_kirby(kirby)
    ice_monster1 = Ice_Monster(background,x_start=background.kbg_x - 370, x_end=background.kbg_x - 180, y=125)
    ice_monster2 = Ice_Monster(background, x_start=background.kbg_x - 100, x_end=background.kbg_x + 90, y=150)
    ice_monster3 = Ice_Monster(background, x_start=background.kbg_x + 560, x_end=background.kbg_x + 750, y=150)

    kirby_world.add_object(background, 1)
    kirby_world.add_object(kirby,1)
    kirby_world.add_object(ice_monster1, 1)
    kirby_world.add_object(ice_monster2, 1)
    kirby_world.add_object(ice_monster3, 1)

    kirby_world.add_collision_pair('kirby:map', kirby, background)
    kirby_world.add_collision_pair('kirby:ice',kirby,ice_monster1)
    kirby_world.add_collision_pair('kirby:ice', kirby, ice_monster2)
    kirby_world.add_collision_pair('kirby:ice', kirby, ice_monster3)
    kirby_world.add_collision_pair('kirby:boss',kirby,0)

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


