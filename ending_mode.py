from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import kirby_game_framework
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time, load_music

def init():
    global image
    global bgm

    image = load_image('Resource\\kirby_ending.png')
    bgm = load_music('Resource\\24. The End (REALLY!).mp3')
    bgm.set_volume(32)
    bgm.repeat_play()

def finish():
    global image

def update():
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
            kirby_game_framework.quit()

def pause(): pass
def resume(): pass