from pico2d import load_image, draw_rectangle
import kirby_game_framework

PIXEL_PER_METER = (10.0 / 0.3)
BACKGROUND_SPEED_KMPH = 20.0  # Km / Hour
BACKGROUND_SPEED_MPM = (BACKGROUND_SPEED_KMPH * 1000.0 / 60.0)
BACKGROUND_SPEED_MPS = (BACKGROUND_SPEED_MPM / 60.0)
BACKGROUND_SPEED_PPS = (BACKGROUND_SPEED_MPS * PIXEL_PER_METER)

class Background_kirby:
    def __init__(self,kirby):
        self.kbg_x = 1000
        self.kirby = kirby
        self.image_map = load_image('level1-1.png')
        self.image = load_image('kirby_background_stage1.png')
    def draw(self):
        self.image.draw(self.kbg_x, 384, 2000, 768)
        if self.kirby.x > 850:
            self.image.draw(self.kbg_x,384,2000,768)
            if self.kbg_x > 200:
                self.kbg_x -= BACKGROUND_SPEED_PPS / 2 * kirby_game_framework.frame_time
            elif self.kbg_x <= 200:
                self.kbg_x += 0
        elif self.kirby.x <= 250:
            self.image.draw(self.kbg_x, 384, 2000, 768)
            if self.kbg_x < 1000:
                self.kbg_x += BACKGROUND_SPEED_PPS / 2 * kirby_game_framework.frame_time
            elif self.kbg_x >= 1000:
                self.kbg_x += 0
        self.image_map.draw(self.kbg_x, 180, 3000, 384)
        draw_rectangle(*self.get_bb())
    def update(self):
        pass

    def get_bb(self):
        return 0 , 0, 2000 , 125