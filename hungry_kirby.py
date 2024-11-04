

from pico2d import*

from kirby import Kirby

# from kirby_background import Background_kirby

Back_WIDTH, Back_HEIGHT = 1024, 768

class Background_kirby:
    def __init__(self):
        global kirby
        self.kbg_x = 1000
        self.image = load_image('kirby_background_stage1.png')
    def draw(self):
        self.image.draw(self.kbg_x, 384, 2000, 768)
        if kirby.x > 850:
            self.image.draw(self.kbg_x,384,2000,768)
            if self.kbg_x > 200:
                self.kbg_x -= 3
            elif self.kbg_x <= 200:
                self.kbg_x += 0
        elif kirby.x <= 250:
            self.image.draw(self.kbg_x, 384, 2000, 768)
            if self.kbg_x < 1000:
                self.kbg_x += 3
            elif self.kbg_x >= 1000:
                self.kbg_x += 0
    def update(self):
        pass

def handle_events():
    global running
    global dir
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        #elif event.type == SDL_KEYDOWN and SDLK_ESCAPE:
            #running = False
        else:
            kirby.handle_event(event)

def reset_world():
    global running
    global kirby
    global world
    global background
    global stage1


    running = True
    world = []

    background = Background_kirby()
    world.append(background)

    kirby = Kirby()
    world.append(kirby)

def update_world():
    for o in world:
        o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas(Back_WIDTH,Back_HEIGHT)
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
# finalization code
close_canvas()
