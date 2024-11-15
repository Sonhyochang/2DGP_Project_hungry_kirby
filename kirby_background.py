from pico2d import load_image, draw_rectangle


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
                self.kbg_x -= 3
            elif self.kbg_x <= 200:
                self.kbg_x += 0
        elif self.kirby.x <= 250:
            self.image.draw(self.kbg_x, 384, 2000, 768)
            if self.kbg_x < 1000:
                self.kbg_x += 3
            elif self.kbg_x >= 1000:
                self.kbg_x += 0
        self.image_map.draw(self.kbg_x, 180, 3000, 384)
        draw_rectangle(*self.get_bb())
    def update(self):
        pass

    def get_bb(self):
        return 0 , 0, 2000 , 125