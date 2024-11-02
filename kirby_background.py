from pico2d import load_image


class Background_kirby:
    def __init__(self):
        self.image = load_image('kirby_background_stage1.png')
    def draw(self):
        self.image.draw(1000,384,2000,768)
    def update(self):
        pass