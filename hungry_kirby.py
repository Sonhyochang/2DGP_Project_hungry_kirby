

from pico2d import open_canvas, delay, close_canvas

import kirby_game_framework

import kirby_play_mode as start_mode

import title_mode


open_canvas(1024,768)
kirby_game_framework.run(title_mode)
close_canvas()
