import time
from pico2d import load_image, get_time, draw_rectangle, load_wav, load_music, clear_canvas
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_SPACE, SDL_KEYUP, SDLK_e

import ice_monster
import kirby_game_framework
import kirby_play_mode
import kirby_world
import title_mode
from kirby_background import Background_kirby
from boss_map import BossMap

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
FRAMES_PER_ACTION_ICE_JUMP = 12
FRAMES_PER_ACTION_ICE_SPACE_JUMP = 9
FRAMES_PER_ACTION_ICE_IDLE = 10

class Kirby:
    vac_sound = None
    change_sound = None
    die_monster_sound = None
    jump_sound = None
    def __init__(self):
        self.x, self.y = 400, 125
        self.life_x , self.life_y = 125,25
        self.ice_hud_x, self.ice_hud_y = 50, 25
        self.frame = 0
        self.life_frame = 0
        self.ice_hud_frame = 0
        self.life_action = 0
        self.ice_hud_action = 0
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
        self.ice_mode = False
        self.attack_mode = False
        self.map = True
        self.sound_play = False
        self.kirby_life = 3
        self.die_sound_playing = False
        self.last_damage_time = 0
        self.damage_cooldown = 10
        self.bgm = load_music('06. Kirby Dance (Short).mp3')
        self.bgm.set_volume(32)


        self.image = load_image('kirby_animation_sheet2.png')
        self.ice_image = load_image('ice_kirby1.png')
        self.life_image = load_image('kirby_life.png')
        self.ice_hud_image = load_image('ice_mode_hud.png')

        self.bgm = load_music('26. Hit!.mp3')
        self.bgm.set_volume(32)

        if not Kirby.vac_sound:
            Kirby.vac_sound = load_wav('vac.wav')
            Kirby.vac_sound.set_volume(16)
        if not Kirby.change_sound:
            Kirby.change_sound = load_wav('cahnge_ice_kirby.wav')
            Kirby.change_sound.set_volume(16)
        if not Kirby.die_monster_sound:
            Kirby.die_monster_sound = load_wav('die_monster.wav')
            Kirby.die_monster_sound.set_volume(16)
        if not Kirby.jump_sound:
            Kirby.jump_sound = load_wav('jump.wav')
            Kirby.jump_sound.set_volume(16)



    def update(self):
        if self.kirby_life == 3:
            self.life_frame = 0
        elif self.kirby_life == 2:
            self.life_frame = 1
        elif self.kirby_life == 1:
            self.life_frame = 2
        elif self.kirby_life == 0:
            self.life_frame = 3
        elif self.kirby_life < 0:
            self.bgm.play()
            music_time = 3
            time.sleep(music_time)
            self.die_sound_playing = False
            kirby_play_mode.finish()
            kirby_game_framework.change_mode(title_mode)


        if self.ice_mode:
            if self.jump:
                if self.space_jump:
                    self.frame = self.frame = (self.frame + FRAMES_PER_ACTION_ICE_SPACE_JUMP * ACTION_PER_TIME * kirby_game_framework.frame_time) % 9
                else:
                    self.frame = self.frame = (self.frame + FRAMES_PER_ACTION_ICE_JUMP * ACTION_PER_TIME * kirby_game_framework.frame_time) % 12
            elif self.damage_mode:
                self.frame = (self.frame + FRAMES_PER_ACTION_DAMAGE * ACTION_PER_TIME * kirby_game_framework.frame_time) % 10
                knockback_per_frame = self.knockback_speed * kirby_game_framework.frame_time
                if self.knockback_distance > 0:
                    self.x +=  self.knockback_dir * knockback_per_frame
                    self.knockback_distance -= knockback_per_frame

                if time.time() - self.damage_start_time > 0.5:
                    self.damage_mode = False
            else:
                self.frame = (self.frame + FRAMES_PER_ACTION_ICE_IDLE * ACTION_PER_TIME * kirby_game_framework.frame_time) % 10

        else:
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
        if self.map:
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
                Kirby.jump_sound.play()
            elif event.key == SDLK_SPACE:
                self.space_jump = True
                self.slow_fall = True
                Kirby.jump_sound.play()
            elif event.key == SDLK_e:
                self.vac_mode = True
                self.sound_play = True
                if self.sound_play:
                    if not self.ice_mode:
                        Kirby.vac_sound.play()
                else:
                    return
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
                self.sound_play = False


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
        if kirby_play_mode.background.kbg_x - 180 < self.x < kirby_play_mode.background.kbg_x + 780:
            if not self.jump:
                self.y = 155
            else:
                self.min_y = 155
                self.max_y = 280
        elif kirby_play_mode.background.kbg_x - 890 < self.x < kirby_play_mode.background.kbg_x - 752:
            if not self.jump:
                self.y = 155
            else:
                self.min_y = 155
                self.max_y = 280
        elif kirby_play_mode.background.kbg_x + 780 < self.x < kirby_play_mode.background.kbg_x + 850:
            if not self.jump:
                self.y = 300
            else:
                self.min_y = 300
                self.max_y = 425
        else:
            if not self.jump:
                self.y = 125
            else:
                self.min_y = 125
                self.max_y = 250


    def draw(self):
        #draw_rectangle(*self.get_bb())
        self.life_image.clip_draw(self.life_frame * 50, self.life_action, 50, 35, self.life_x, self.life_y, 100, 100)
        if not self.ice_mode:
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

            if self.jump and not self.vac_mode and not self.damage_mode:
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

            if self.vac_mode and not self.jump and not self.damage_mode:
                if self.dir == 0:
                    if self.kirby_face_dir == 1:
                        self.image.clip_draw(815 + int(self.frame) * 30, self.action * 34 - 175, 30, 34, self.x, self.y, 55, 55)
                    elif self.kirby_face_dir == -1:
                        self.image.clip_composite_draw(815 + int(self.frame) * 30, self.action * 34 - 175, 30, 34, 0, 'h', self.x, self.y, 55, 55)
                elif self.dir == 1:
                    self.vac_mode = False
                elif self.dir == -1:
                    self.vac_mode = False

            if self.damage_mode and not self.jump and not self.vac_mode:
                if self.knockback_dir == 1:
                    self.image.clip_composite_draw(510 + int(self.frame) * 25, self.action * 34 - 309, 25, 34, 0, 'h',self.x,self.y,55,55)
                elif self.knockback_dir == -1:
                    self.image.clip_draw(510 + int(self.frame) * 25, self.action * 34 - 309, 25, 34, self.x, self.y,55, 55)
                    #self.damage_mode = False
        elif self.ice_mode:
            self.ice_hud_image.clip_draw(self.ice_hud_frame * 42, self.ice_hud_action * 57, 42,57,self.ice_hud_x,self.ice_hud_y,100,100)
            if not self.jump and not self.vac_mode and not self.damage_mode:
                if self.dir == 0:
                    if self.kirby_face_dir == 1:
                        self.ice_image.clip_composite_draw(int(self.frame) * 30, self.action * 36, 30, 36, 0, 'h',self.x, self.y, 50, 50)
                    elif self.kirby_face_dir == -1:
                        self.ice_image.clip_draw(int(self.frame) * 30, self.action * 36, 30, 36, self.x, self.y, 50, 50)
                elif self.dir == 1:
                    self.ice_image.clip_composite_draw(int(self.frame) * 33, self.action * 36 - 36, 33, 36, 0, 'h',self.x, self.y, 50, 50)
                elif self.dir == -1:
                    self.ice_image.clip_draw(int(self.frame) * 33, self.action * 36 - 36, 33, 36, self.x, self.y, 50,50)

            if self.jump:
                if self.dir2 == -1:
                    if self.space_jump:
                        self.ice_image.clip_draw(int(self.frame) * 40, self.action * 36 - 150, 40, 36, self.x, self.y, 50, 50)
                    else:
                        self.ice_image.clip_draw(int(self.frame) * 33, self.action * 36 - 110, 33, 36, self.x, self.y, 50,50)
                elif self.dir2 == 0:
                    if self.space_jump:
                        if self.kirby_face_dir == 1:
                            self.ice_image.clip_composite_draw(int(self.frame) * 40, self.action * 36 - 150, 40, 36, 0, 'h',self.x, self.y, 50, 50)
                        elif self.kirby_face_dir == -1:
                            self.ice_image.clip_draw(int(self.frame) * 40, self.action * 36 - 150, 40, 36, self.x,self.y, 50, 50)
                    else:
                        self.ice_image.clip_draw(int(self.frame) * 33, self.action * 36 - 110, 33, 36, self.x, self.y,50, 50)
                elif self.dir2 == 1:
                    if self.space_jump:
                        self.ice_image.clip_composite_draw(int(self.frame) * 40, self.action * 36 - 150, 40, 36, 0, 'h',self.x, self.y, 50, 50)
                    else:
                        self.ice_image.clip_composite_draw(int(self.frame) * 33, self.action * 36 - 110, 33, 36, 0, 'h',self.x, self.y, 50, 50)

            if self.vac_mode:
                if self.dir == 0:
                    if self.kirby_face_dir == 1:
                        self.ice_image.clip_composite_draw(int(self.frame) * 110, self.action * 40 - 300, 110, 40, 0, 'h', self.x, self.y, 150, 65)
                    elif self.kirby_face_dir == -1:
                        self.ice_image.clip_draw(int(self.frame) * 110, self.action * 40 - 300, 110, 40, self.x, self.y, 150, 65)
                elif self.dir == 1:
                    self.vac_mode = False
                elif self.dir == -1:
                    self.vac_mode = False

            if self.damage_mode and not self.jump and not self.vac_mode:
                if self.knockback_dir == 1:
                    self.image.clip_composite_draw(510 + int(self.frame) * 25, self.action * 34 - 309, 25, 34, 0, 'h',self.x,self.y,55,55)
                elif self.knockback_dir == -1:
                    self.image.clip_draw(510 + int(self.frame) * 25, self.action * 34 - 309, 25, 34, self.x, self.y,55, 55)

    def get_bb(self):
        if self.ice_mode and self.vac_mode:
            if self.kirby_face_dir == -1:
                return self.x - 70, self.y - 24, self.x + 27, self.y + 24
            elif self.kirby_face_dir == 1:
                return self.x - 24, self.y - 24, self.x + 70, self.y +24
        else:
            return self.x - 27, self.y - 24, self.x + 27, self.y + 24

    def handle_collision(self, group, other):
        current_time = time.time()
        if group == 'kirby:map':
            self.map = False
            self.x = 200
            self.y = 170
            self.max_y = 295
            self.min_y = 170
        elif group == 'kirby:ice':
            if self.vac_mode and not self.ice_mode:
                self.ice_mode = True
                Kirby.change_sound.play()
            elif self.ice_mode:
                if self.vac_mode:
                    Kirby.die_monster_sound.play()
            else:
                self.damage_mode = True
                self.die_sound_playing = True
                self.damage_start_time = time.time()
                self.knockback_distance = 100
                if other.x < self.x:
                     self.knockback_dir = 1 # 우
                else:
                    self.knockback_dir = -1 # 좌
                if self.die_sound_playing:
                    Kirby.die_monster_sound.play()
                self.kirby_life -= 1
        elif group == 'kirby:boss':
            if self.ice_mode:
                if hasattr(other,'boss_hp') and other.boss_hp <= 0:
                    self.bgm = load_music('06. Kirby Dance (Short).mp3')
                    self.bgm.set_volume(32)
                    self.bgm.play()
                    pass
                else:
                    if self.vac_mode:
                        other.damage()
                        Kirby.die_monster_sound.play()
                    else:
                        if self.damage_mode == False and current_time - self.last_damage_time >= self.damage_cooldown:
                            self.damage_mode = True
                            self.die_sound_playing = True
                            self.damage_start_time = time.time()
                            self.knockback_distance = 100
                            if other.x < self.x:
                                self.knockback_dir = 1  # 우
                            else:
                                self.knockback_dir = -1  # 좌
                            if self.die_sound_playing:
                                Kirby.die_monster_sound.play()
                            self.kirby_life -= 1
            else:
                if self.damage_mode == False and current_time - self.last_damage_time >= self.damage_cooldown:
                    self.damage_mode = True
                    self.die_sound_playing = True
                    self.damage_start_time = time.time()
                    self.knockback_distance = 100
                    if other.x < self.x:
                        self.knockback_dir = 1  # 우
                    else:
                        self.knockback_dir = -1  # 좌
                    if self.die_sound_playing:
                        Kirby.die_monster_sound.play()
                    self.kirby_life -= 1



