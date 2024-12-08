from pico2d import *

import kirby_game_framework

PIXEL_PER_METER = (10.0 / 0.3)
BACKGROUND_SPEED_KMPH = 20.0  # Km / Hour
BACKGROUND_SPEED_MPM = (BACKGROUND_SPEED_KMPH * 1000.0 / 60.0)
BACKGROUND_SPEED_MPS = (BACKGROUND_SPEED_MPM / 60.0)
BACKGROUND_SPEED_PPS = (BACKGROUND_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class BossMap:
        def __init__(self):
            self.x, self.y = 512, 384
            self.frame = 0
            self.action= 2
            self.image = load_image('Resource\\dedede_area.png')
            self.bgm = load_music('Resource\\09. King Dedede.mp3')
            self.bgm.set_volume(32)
            self.bgm.repeat_play()

        def draw(self):
            #draw_rectangle(*self.get_bb())
            self.image.clip_draw(int(self.frame) * 256, self.action * 205,256,205,self.x,self.y,1024,768)

        def update(self):
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * kirby_game_framework.frame_time) % 4


        def get_bb(self):
            return self.x - 200, self.y - 150, self.x + 200, self.y + 205

        def handle_collision(self, group, other):
            pass