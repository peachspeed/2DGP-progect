import a_game_framework
import a_title_mode
from pico2d import *

def init():
    global image, logo_start_time
    image = load_image('roding1.png')
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    global logo_start_time
    if get_time() - logo_start_time > 2.0:  # 2초 후 타이틀로 전환
        a_game_framework.change_mode(a_title_mode)

def draw():
    clear_canvas()
    image.draw(900, 450)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            a_game_framework.quit()
