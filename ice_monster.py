import kirby_background
import kirby_game_framework

from pico2d import *
import time

import kirby_play_mode
import kirby_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Ice_Monster:
    def __init__(self,background,x_start,x_end,y):
        self.y = y
        self.background = background
        self.x_start = x_start
        self.x_end = x_end
        self.x = x_start
        self.action = 3
        self.frame = 0
        self.image = load_image('ice_monster.png')
        self.dir = 1

    def update(self):
        self.action = 3
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * kirby_game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += (RUN_SPEED_PPS / 2) * self.dir * kirby_game_framework.frame_time
        # 1번째 몬스터
        # if self.x > self.background.kbg_x - 180:
        #     self.dir = -1
        # elif self.x < self.background.kbg_x - 370:
        #     self.dir = 1
        # self.x = clamp(self.background.kbg_x - 370 ,self.x, self.background.kbg_x - 180)

        # 2번쨰 몬스터
        # if self.x > self.background.kbg_x + 90:
        #     self.dir = -1
        # elif self.x < self.background.kbg_x - 100:
        #     self.dir = 1
        # self.x = clamp(self.background.kbg_x - 100 ,self.x, self.background.kbg_x + 90)

        # 3번째 몬스터
        # if self.x > self.background.kbg_x + 750:
        #     self.dir = -1
        # elif self.x < self.background.kbg_x + 560:
        #     self.dir = 1
        # self.x = clamp(self.background.kbg_x + 560 ,self.x, self.background.kbg_x + 750)

        if self.x > self.x_end:
            self.dir = -1
        elif self.x < self.x_start:
            self.dir = 1
        self.x = clamp(self.x_start ,self.x, self.x_end)




    def draw(self):
        #draw_rectangle(*self.get_bb())
        if self.dir > 0:
            self.image.clip_composite_draw(68 + int(self.frame) * 30, 10 + self.action * 30, 30, 31, 0, 'h', self.x, self.y, 50, 50)
        else:
            self.image.clip_draw(68 + int(self.frame) * 30, 10 + self.action * 30, 30, 31, self.x, self.y, 50, 50)


    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15


    def handle_collision(self, group, other):
        if group == 'kirby:ice':
            kirby_world.remove_object(self)
            pass

