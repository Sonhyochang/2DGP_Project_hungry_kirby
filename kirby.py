import time
from pico2d import load_image, get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_SPACE, SDL_KEYUP, SDLK_e

import ice_monster
import kirby_game_framework
import kirby_play_mode
import kirby_world
from boss_map import BossMap
from ice_kirby import Ice_Kirby

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
FRAMES_PER_ACTION_DAMAGE = 10
FRAMES_PER_ACTION_ICE_RUN = 10
FRAMES_PER_ACTION_ICE_IDLE = 2

class Kirby:
    def __init__(self):
        self.x, self.y = 400, 125
        self.frame = 0
        self.dir = 0
        self.dir2 = 0
        self.dir3 = 0
        self.action = 9
        self.min_y = 125
        self.max_y = 250
        self.kirby_face_dir = 1
        self.jump = False
        self.high = False
        self.space_jump = False
        self.slow_fall = False
        self.vac_mode = False
        self.damage_mode = False
        self.damage_start_time = 0
        self.knockback_distance = 100
        self.knockback_speed = 200
        self.knockback_dir = 0

        self.image = load_image('kirby_animation_sheet2.png')



    def update(self):
        if self.space_jump:
              self.frame = (self.frame + FRAMES_PER_ACTION_JUMP * ACTION_PER_TIME * kirby_game_framework.frame_time) % 6
        elif self.vac_mode:
            self.frame = (self.frame + FRAMES_PER_ACTION_VAC * ACTION_PER_TIME * kirby_game_framework.frame_time) % 5
        elif self.damage_mode:
            self.frame = (self.frame + FRAMES_PER_ACTION_DAMAGE * ACTION_PER_TIME * kirby_game_framework.frame_time) % 10
            knockback_per_frame = self.knockback_speed * kirby_game_framework.frame_time
            if self.knockback_distance > 0:
                self.x +=  self.knockback_dir * knockback_per_frame
                self.knockback_distance -= knockback_per_frame

            if time.time() - self.damage_start_time > 0.5:
                self.damage_mode = False
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION_BASE * ACTION_PER_TIME * kirby_game_framework.frame_time) % 9

        #self.frame = 3
        self.move_limit()
        self.jump_logic()
        self.map_up()

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
                if self.y >= self.max_y:
                    self.high = False
            else:
                if self.space_jump:
                    self.y += (JUMP_SPEED_PPS / 3) * kirby_game_framework.frame_time
                elif self.slow_fall:
                    self.y -= (JUMP_SPEED_PPS / 3) * kirby_game_framework.frame_time
                else:
                    self.y -= JUMP_SPEED_PPS * kirby_game_framework.frame_time

            if self.y <= self.min_y:
                self.y = self.min_y
                self.jump = False
                self.space_jump = False
                self.dir2 = 0

    def map_up(self):
        if kirby_play_mode.background.kbg_x - 890 < self.x <  kirby_play_mode.background.kbg_x - 752:
            if not self.jump:  # 점프 중이 아닐 때만 y값을 변경
                self.min_y = 150
                self.max_y = 275
                self.y = max(self.y, self.min_y)  # y가 min_y보다 작지 않도록 제한
                self.y = min(self.y, self.max_y)  # y가 max_y보다 크지 않도록 제한
        elif kirby_play_mode.background.kbg_x - 160 < self.x <  kirby_play_mode.background.kbg_x + 30:
            if not self.jump:  # 점프 중이 아닐 때만 y값을 변경
                self.min_y = 150
                self.max_y = 275
                self.y = max(self.y, self.min_y)  # y가 min_y보다 작지 않도록 제한
                self.y = min(self.y, self.max_y)  # y가 max_y보다 크지 않도록 제한
        elif kirby_play_mode.background.kbg_x + 25 < self.x <  kirby_play_mode.background.kbg_x + 140:
            if not self.jump:  # 점프 중이 아닐 때만 y값을 변경
                self.min_y = 230
                self.max_y = 355
                self.y = max(self.y, self.min_y)  # y가 min_y보다 작지 않도록 제한
                self.y = min(self.y, self.max_y)  # y가 max_y보다 크지 않도록 제한
        elif kirby_play_mode.background.kbg_x + 320 < self.x <  kirby_play_mode.background.kbg_x + 780:
            if not self.jump:  # 점프 중이 아닐 때만 y값을 변경
                self.min_y = 155
                self.max_y = 280
                self.y = max(self.y, self.min_y)  # y가 min_y보다 작지 않도록 제한
                self.y = min(self.y, self.max_y)  # y가 max_y보다 크지 않도록 제한
        elif kirby_play_mode.background.kbg_x + 780 < self.x <  kirby_play_mode.background.kbg_x + 850:
            if not self.jump:  # 점프 중이 아닐 때만 y값을 변경
                self.min_y = 300
                self.max_y = 425
                self.y = max(self.y, self.min_y)  # y가 min_y보다 작지 않도록 제한
                self.y = min(self.y, self.max_y)  # y가 max_y보다 크지 않도록 제한
        else:
            if not self.jump:  # 점프 중이 아닐 때만 y값을 기본값으로 설정
                self.y = 125
                self.min_y = 125
                self.max_y = 250

    def draw(self):
        draw_rectangle(*self.get_bb())
        if not self.jump and not self.vac_mode and not self.damage_mode:
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

        if self.damage_mode:
            if self.knockback_dir == 1:
                self.image.clip_composite_draw(510 + int(self.frame) * 25, self.action * 34 - 309, 25, 34, 0, 'h',self.x,self.y,55,55)
            elif self.knockback_dir == -1:
                self.image.clip_draw(510 + int(self.frame) * 25, self.action * 34 - 309, 25, 34, self.x, self.y,55, 55)
                #self.damage_mode = False

    def get_bb(self):
            return self.x - 27, self.y - 24, self.x + 27, self.y + 24

    def handle_collision(self, group, other):
        if group == 'kirby:map':
            self.x = 400
            self.y = 175
            self.min_y = 175
            self.max_y = 350
        elif group == 'kirby:ice':
            self.damage_mode = True
            self.damage_start_time = time.time()
            self.knockback_distance = 100
            if other.x < self.x:
                 self.knockback_dir = 1 # 우
            else:
                self.knockback_dir = -1 # 좌




