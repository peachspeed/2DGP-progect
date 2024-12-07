import a_game_framework
import a_clothes
from pico2d import *

def init():
    global image
    image = load_image('title.png')

def finish():
    global image
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            a_game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_1:
                a_game_framework.change_mode(a_clothes)

def draw():
    clear_canvas()
    image.draw(900, 450)
    update_canvas()

def update():
    pass
