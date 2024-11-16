import time

from pico2d import load_image, get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_SPACE, SDL_KEYUP, SDLK_e

import kirby_game_framework
import kirby_world

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
PIXEL_PER_HEIGHT = (74.0 / 2.2)
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
JUMP_SPEED_KMPH = 40.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_HEIGHT)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_BASE = 9
FRAMES_PER_ACTION_JUMP = 6
FRAMES_PER_ACTION_VAC = 5

class Kirby:
    def __init__(self):
        self.x, self.y = 400, 125
        self.frame = 0
        self.dir = 0
        self.dir2 = 0
        self.dir3 = 0
        self.action = 9
        self.kirby_face_dir = 1
        self.jump = False
        self.high = False
        self.space_jump = False
        self.slow_fall = False
        self.vac_mode = False

        self.image = load_image('kirby_animation_sheet2.png')

    def update(self):

        if self.space_jump:
              self.frame = (self.frame + FRAMES_PER_ACTION_JUMP * ACTION_PER_TIME * kirby_game_framework.frame_time) % 6
        elif self.vac_mode:
            self.frame = (self.frame + FRAMES_PER_ACTION_VAC * ACTION_PER_TIME * kirby_game_framework.frame_time) % 5
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION_BASE * ACTION_PER_TIME * kirby_game_framework.frame_time) % 9

        #self.frame = 3
        self.move_limit()
        self.jump_logic()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir = 1
                self.kirby_face_dir = 1
                if self.jump:
                    self.dir2 = 1
            elif event.key == SDLK_LEFT:
                self.dir = -1
                self.kirby_face_dir = -1
                if self.jump:
                    self.dir2 = -1
            elif event.key == SDLK_UP:
                if self.dir == -1:
                    self.dir2 = -1
                elif self.dir == 1:
                    self.dir2 = 1
                elif self.dir == 0:
                    self.dir2 = self.kirby_face_dir
                self.jump = True
                self.high = True
            elif event.key == SDLK_SPACE:
                self.space_jump = True
                self.slow_fall = True
            elif event.key == SDLK_e:
                self.vac_mode = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.dir = 0
            elif event.key == SDLK_LEFT:
                self.dir = 0
            # elif event.key == SDLK_UP:
            #     self.dir2 = 0
            elif event.key == SDLK_SPACE:
                self.space_jump = False
                self.slow_fall = False
            elif event.key == SDLK_e:
                self.vac_mode = False

    def move_limit(self):
        if 1024 > self.x > 0:
            self.x += self.dir * RUN_SPEED_PPS * kirby_game_framework.frame_time
        elif self.x >= 1024:
            self.x = self.x - 10
        elif self.x <= 0:
            self.x = self.x + 10

    def jump_logic(self):
        if self.jump:
            if self.high:
                self.y += JUMP_SPEED_PPS * kirby_game_framework.frame_time
                if self.y >= 250:
                    self.high = False
            else:
                if self.space_jump:
                    self.y += 5
                elif self.slow_fall:
                    self.y -= 5
                else:
                    self.y -= JUMP_SPEED_PPS * kirby_game_framework.frame_time

            if self.y <= 125:
                self.y = 125
                self.jump = False
                self.space_jump = False
                self.dir2 = 0

    def draw(self):
        draw_rectangle(*self.get_bb())
        if not self.jump and not self.vac_mode:
            if self.dir == 0:
                if self.kirby_face_dir == 1:
                    self.image.clip_draw(199 + int(self.frame) * 28, self.action * 34 - 309, 28, 34, self.x, self.y,60, 60)
                elif self.kirby_face_dir == -1:
                    self.image.clip_composite_draw(199 + int(self.frame) * 28, self.action * 34 -309, 28, 34, 0, 'h', self.x, self.y, 60,60)
            elif self.dir == 1:
                self.image.clip_draw(79 + int(self.frame) * 23, self.action * 34, 23, 34, self.x, self.y, 50, 50)
            elif self.dir == -1:
                self.image.clip_composite_draw(79 + int(self.frame) * 23, self.action * 34, 23, 34, 0, 'h', self.x, self.y, 50, 50)

        if self.jump:
            if self.dir2 == -1:
                if self.space_jump:
                    self.image.clip_composite_draw(474 + int(self.frame) * 30, self.action * 34 - 34, 30, 34, 0, 'h', self.x,
                                                   self.y, 50, 50)
                else:
                    self.image.clip_composite_draw(644 + int(self.frame) * 25, self.action * 34, 24, 34, 0, 'h', self.x,
                                                   self.y, 50, 50)
            elif self.dir2 == 0:
                if self.space_jump:
                    if self.kirby_face_dir == 1:
                        self.image.clip_draw(474 + int(self.frame) * 30, self.action * 34 - 34, 30, 34, self.x, self.y, 50, 50)
                    elif self.kirby_face_dir == -1:
                        self.image.clip_composite_draw(474 + int(self.frame) * 30, self.action * 34 - 34, 30, 34, 0,
                                                       'h', self.x,
                                                       self.y, 50, 50)
                else:
                    self.image.clip_draw(644 + int(self.frame) * 25, self.action * 34, 24, 34, self.x, self.y, 50, 50)
            elif self.dir2 == 1:
                if self.space_jump:
                    self.image.clip_draw(474 + int(self.frame) * 30, self.action * 34 - 34, 30, 34, self.x, self.y, 50, 50)
                else:
                    self.image.clip_draw(644 + int(self.frame) * 25, self.action * 34, 24, 34, self.x, self.y, 50, 50)

        if self.vac_mode:
            if self.dir == 0:
                if self.kirby_face_dir == 1:
                    self.image.clip_draw(815 + int(self.frame) * 30, self.action * 34 - 175, 30, 34, self.x, self.y, 55, 55)
                elif self.kirby_face_dir == -1:
                    self.image.clip_composite_draw(815 + int(self.frame) * 30, self.action * 34 - 175, 30, 34, 0, 'h', self.x, self.y, 55, 55)
            elif self.dir == 1:
                self.vac_mode = False
            elif self.dir == -1:
                self.vac_mode = False
    def get_bb(self):
        return self.x - 27, self.y - 24, self.x + 27, self.y + 24