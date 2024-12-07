from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import kirby_game_framework
import kirby_play_mode
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time, load_music

def init():
    global image
    global bgm
    # global running
    # global title_start_time

    image = load_image('kirby_title.png')
    bgm = load_music('01. Ttile Screen.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()
    # running = True
    # title_start_time = get_time()

def finish():
    global image
    # del image

def update():
    # global title_start_time
    # if get_time() - title_start_time >= 2.0:
    #     title_start_time = get_time()
    #     kirby_game_framework.change_mode(kirby_play_mode)
    pass

def draw():
    clear_canvas()
    image.draw(512,384,1024,768)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            kirby_game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            kirby_game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            kirby_game_framework.change_mode(kirby_play_mode)

def pause(): pass
def resume(): pass


