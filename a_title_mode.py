from pico2d import*
from sdl2 import SDLK_ESCAPE
import a_game_framework


def init():
    global image
    image = load_image('back.png')


def finish():
    global image
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            a_game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            a_game_framework.quit()

def draw():
    clear_canvas()
    image.draw(300, 400)
    update_canvas()

def update():
    pass