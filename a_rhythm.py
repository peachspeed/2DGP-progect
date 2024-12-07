from pico2d import *

def init():
    global background, notes, score, line_y, game_started
    background = load_image('backrythem.png')
    notes = []
    score = 0
    line_y = 150
    game_started = False

def finish():
    global background, notes
    del background, notes

def handle_events():
    global game_started
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_started = True

def draw():
    clear_canvas()
    background.draw(900, 450)
    if game_started:
        for note in notes:
            note.draw()
    update_canvas()

def update():
    if game_started:
        for note in notes:
            note.update()
