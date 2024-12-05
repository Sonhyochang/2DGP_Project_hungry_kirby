import time

import kirby_game_framework

from pico2d import *
import random

import kirby_play_mode
from behavior_tree import BehaviorTree, Action

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
TIME_PER_ACTION_ATTACK = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
ACTION_PER_TIME_ATTACK = 1.0 / TIME_PER_ACTION_ATTACK
FRAMES_PER_ACTION_IDLE = 5
FRAMES_PER_ACTION_RUN = 3
FRAMES_PER_ACTION_ATTACK = 3

class Boss_Monster:
    IDLE, RUN, ATTACK = 0, 1 ,2
    def __init__(self):
        self.x, self.y = 1024,290
        self.action = 3
        self.frame = 0
        self.image = load_image('deded_boss.png')
        self.dir = 1
        self.state = self.IDLE
        self.tx, self.ty = 0, 0
        self.total_frame = {self.IDLE: 4,self.RUN: 3, self.ATTACK: 3}
        self.attack_range = 300
        self.can_attack = True  # 공격 가능 여부
        self.attack_cooldown = 3.0  # 쿨타임 (초)
        self.last_attack_time = 0.0  # 마지막 공격 시간 기록

    def update(self):
        print(f"State: {self.state}, Frame: {self.frame}")
        current_time = time.time()

        distance = math.sqrt((self.x - kirby_play_mode.kirby.x) ** 2 + (self.y - kirby_play_mode.kirby.y) ** 2)

        if distance <= self.attack_range:  # 커비가 범위 안에 있으면
            if kirby_play_mode.kirby.x < self.x:  # 커비가 왼쪽에 있으면
                self.dir = -1
            else:  # 커비가 오른쪽에 있으면
                self.dir = 1

            if self.can_attack:
                self.state = self.ATTACK
                self.can_attack = False
                self.last_attack_time = current_time
            elif current_time - self.last_attack_time >= self.attack_cooldown:
                self.can_attack = True
        else:
            self.state = self.RUN

        if self.state == self.IDLE:
            self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * kirby_game_framework.frame_time) % FRAMES_PER_ACTION_IDLE
            self.idle_behavior()
        elif self.state == self.RUN:
            self.frame = (self.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * kirby_game_framework.frame_time) % FRAMES_PER_ACTION_RUN
            self.run_behavior()
        elif self.state == self.ATTACK:
            self.frame = ( self.frame + FRAMES_PER_ACTION_ATTACK * ACTION_PER_TIME_ATTACK * kirby_game_framework.frame_time) % FRAMES_PER_ACTION_ATTACK
            self.attack_behavior()

        if int(self.frame) == self.total_frame[self.state]:
            print("Changing state...")
            #self.change_state()


    def change_state(self):
        if self.state == self.IDLE:
            self.state = self.RUN
        elif self.state == self.RUN:
            self.state = self.ATTACK
        elif self.state == self.ATTACK:
            self.state = self.RUN

        self.frame = 0
    def idle_behavior(self):
        pass

    def run_behavior(self):
        self.x += RUN_SPEED_PPS * self.dir * kirby_game_framework.frame_time
        if self.x > 1024:
            self.dir = -1
        elif self.x < 0:
            self.dir = 1
        self.x = clamp(0, self.x, 1024)

    def attack_behavior(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.state == self.IDLE:
            if self.dir > 0:
                self.image.clip_draw(7 + int(self.frame) * 46, self.action * 58 - 130, 46, 58, self.x, self.y + 30, 300, 300)
                self.image.clip_draw(8 + int(self.frame) * 57, 25 + self.action * 58,57,58,self.x,self.y,300,300)
            elif self.dir < 0:
                self.image.clip_composite_draw(7 + int(self.frame) * 46, self.action * 58 - 130,46,58,0,'h',self.x,self.y + 30, 300,300)
                self.image.clip_composite_draw(8 + int(self.frame) * 57, 25 + self.action * 58, 57,58,0,'h',self.x,self.y,300,300)

        elif self.state == self.ATTACK:
            if self.dir > 0:
                self.image.clip_draw(290 + int(self.frame) * 95, self.action * 120 - 350, 95, 120, self.x,self.y,450,450)
            elif self.dir < 0:
                self.image.clip_composite_draw(290 + int(self.frame) * 95, self.action * 120 -350, 95, 120,0,'h',self.x,self.y,450,450)


        elif self.state == self.RUN:
            if self.dir > 0:
                self.image.clip_draw(7 + int(self.frame) * 46, self.action * 58 - 130, 46, 58, self.x + 10, self.y + 115, 300, 300)
                self.image.clip_draw(298 + int(self.frame) * 61, 25 + self.action * 58, 61, 58, self.x, self.y, 300, 300)
            elif self.dir < 0:
                self.image.clip_composite_draw(7 + int(self.frame) * 46, self.action * 58 - 130, 46, 58, 0, 'h', self.x + 10, self.y + 115, 300, 300)
                self.image.clip_composite_draw(298 + int(self.frame) * 61, 25 + self.action * 58, 61, 58,0,'h',self.x,self.y,300,300)
        pass

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 200, self.y - 200, self.x + 200, self.y + 150


    def handle_collision(self, group, other):
        if group == 'kirby:boss':
            pass

