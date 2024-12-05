import a_game_framework
from pico2d import*
import a_title_mode

def init():
    global image
    global running
    global logo_start_time


    open_canvas(1800, 900)
    image = load_image('roding1.png')
    running = True
    logo_start_time = get_time()

def finish():
    global image
    del image


def update():
    global logo_start_time
    if get_time() - logo_start_time >= 2.0:
        a_game_framework.change_mode(a_title_mode)  # 타이틀 모드로 전환


def draw():
    clear_canvas()
    image.draw(900, 450)  # 캔버스 중심(900, 450)에 배경 이미지를 배치
    update_canvas()

def handle_events():
    events = get_events()