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
        draw_rectangle(*self.get_bb1())
        draw_rectangle(*self.get_bb2())
        draw_rectangle(*self.get_bb3())
        draw_rectangle(*self.get_bb4())
        draw_rectangle(*self.get_bb5())
        draw_rectangle(*self.get_bb6())
    def update(self):
        pass

    def get_bb(self):
        return self.kbg_x - 1000 , 0, self.kbg_x - 160 , 100

    def get_bb1(self):
        return self.kbg_x - 890, 100, self.kbg_x - 752, 130

    def get_bb2(self):
        return self.kbg_x - 410, 100, self.kbg_x - 385, 130

    def get_bb3(self):
        return self.kbg_x - 160, 100, self.kbg_x + 30, 130

    def get_bb4(self):
        return self.kbg_x + 25, 130, self.kbg_x + 140, 215

    def get_bb5(self):
        return self.kbg_x + 320, 0, self.kbg_x + 780, 135

    def get_bb6(self):
        return self.kbg_x + 780, 130, self.kbg_x + 850, 280

    def handle_collision(self,group,other):
        if group == 'kirby:map':
            print('collision: map')



