from pico2d import*
import random


class Kirby:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.dir2 = 0
        self.action = 9
        self.jump = False
        self.high = True
        self.image = load_image('kirby_animation_sheet2.png')

    def update(self):
        #pass
        self.frame = (self.frame + 1) % 9
        self.move_limit()
        self.jump_logic()


    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir += 1
            elif event.key == SDLK_LEFT:
                self.dir -= 1
            elif event.key == SDLK_UP:
                self.dir2 = 1
                self.jump = True
                self.high = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.dir -= 1
            elif event.key == SDLK_LEFT:
                self.dir += 1
            elif event.key == SDLK_UP:
                self.dir2 = 0

    def move_limit(self):
        if 800 > self.x > 0:
            self.x += self.dir * 10
        elif self.x >= 800:
            self.x = self.x - 10
        elif self.x <= 0:
            self.x = self.x + 10

    def jump_logic(self):
        if self.jump:
            if self.high:
                self.y += 20
                if self.y >= 250:
                    self.high = False
            else:
                self.y -= 20

            if self.y <= 90:
                self.y = 90
                self.jump = False



    def draw(self):
        if not self.jump and self.dir == 0:
            self.image.clip_draw(79 + self.frame * 23 , self.action * 34, 23, 34, self.x, self.y,50,50)
        elif not self.jump and self.dir > 0:
            self.image.clip_draw(79 + self.frame * 23 , self.action * 34, 23, 34, self.x, self.y,50,50)
        elif not self.jump and self.dir < 0:
            self.image.clip_composite_draw(79 + self.frame * 23, self.action * 34, 23, 34, 0, 'h', self.x, self.y, 50, 50)

        if self.jump and self.dir2 == 0:
            self.image.clip_draw(644 + self.frame * 25, self.action * 34, 24, 34, self.x, self.y, 50, 50)
        elif self.dir2 > 0:
            self.image.clip_draw(644 + self.frame * 25 , self.action * 34, 24, 34, self.x, self.y,50,50)


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


    running = True
    world = []

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

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
# finalization code
close_canvas()
