from pico2d import *
import random

def init():
    global background, button, current_image, click_count, max_clicks
    background = load_image('Backcl.png')
    button = load_image('button.png')
    current_image = None
    click_count = 0
    max_clicks = 6

def finish():
    global background, button, current_image
    del background, button, current_image

def handle_events():
    global current_image, click_count
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 900 - event.y
            if 800 - 50 <= x <= 800 + 50 and 100 - 25 <= y <= 100 + 25:
                if click_count < max_clicks:
                    current_image = pick_item()
                    click_count += 1

def draw():
    clear_canvas()
    background.draw(900, 450)
    if current_image:
        current_image.draw(900, 450)
    button.draw(800, 100)
    update_canvas()

def update():
    pass
