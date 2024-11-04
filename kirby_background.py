from pico2d import load_image

from kirby import Kirby


# class Background_kirby:
#     def __init__(self):
#         global kirby
#         self.kbg_x = 1000
#         self.image = load_image('kirby_background_stage1.png')
#     def draw(self):
#         if kirby.x > 700:
#             self.image.draw(self.kbg_x,384,2000,768)
#             self.kbg_x -= 10
#         elif kirby.x <= 300:
#             self.image.draw(self.kbg_x, 384, 2000, 768)
#             self.kbg_x += 10
#     def update(self):
#         pass