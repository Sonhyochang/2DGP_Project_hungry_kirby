from pico2d import load_image, draw_rectangle, load_music

import kirby_game_framework
import kirby_world
from boss_map import BossMap
from boss_monster import Boss_Monster


PIXEL_PER_METER = (10.0 / 0.3)
BACKGROUND_SPEED_KMPH = 20.0  # Km / Hour
BACKGROUND_SPEED_MPM = (BACKGROUND_SPEED_KMPH * 1000.0 / 60.0)
BACKGROUND_SPEED_MPS = (BACKGROUND_SPEED_MPM / 60.0)
BACKGROUND_SPEED_PPS = (BACKGROUND_SPEED_MPS * PIXEL_PER_METER)

class Background_kirby:
    def __init__(self,kirby):
        self.kbg_x = 1000
        self.kirby = kirby
        self.image_map = load_image('Resource\\level1-1.png')
        self.image = load_image('Resource\\kirby_background_stage1.png')
        self.bgm = load_music('Resource\\04. Prism Plains.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()
        self.boss_map = None
        self.boss = None

    def draw(self):
        self.image.draw(self.kbg_x, 384, 2000, 768)
        if self.kirby.x > 850:
            self.image.draw(self.kbg_x,384,2000,768)
            if self.kbg_x > 200:
                self.kbg_x -= BACKGROUND_SPEED_PPS / 2 * kirby_game_framework.frame_time
            elif self.kbg_x <= 200:
                self.kbg_x = 200
        elif self.kirby.x <= 250:
            self.image.draw(self.kbg_x, 384, 2000, 768)
            if self.kbg_x < 1000:
                self.kbg_x += BACKGROUND_SPEED_PPS / 2 * kirby_game_framework.frame_time
            elif self.kbg_x >= 1000:
                self.kbg_x = 1000
        self.image_map.draw(self.kbg_x, 180, 3000, 384)
        #draw_rectangle(*self.get_bb())
    def update(self):
        pass

    def get_bb(self):
        return self.kbg_x + 800, 280, self.kbg_x + 820, 330

    def handle_collision(self,group,other):
        if group == 'kirby:map':
            self.bgm.stop()
            boss_map = BossMap()
            boss = Boss_Monster()
            kirby_world.add_object(boss_map,0)
            kirby_world.add_object(boss,1)
            kirby_world.add_collision_pair('kirby:boss',0,boss)
            kirby_world.remove_object(self)
            pass


