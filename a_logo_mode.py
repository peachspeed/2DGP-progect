import a_game_framework
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time

def init():
    global image
    global running
    global logo_start_time

    image = load_image('roding1.png')
    running = True
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    global running
    global logo_start_time
    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        a_game_framework.quit()
        running = False

def draw():
    clear_canvas()
    image.draw(300, 400)
    update_canvas()
def handle_events():
    events = get_events()