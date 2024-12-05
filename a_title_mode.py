from pico2d import *
import a_game_framework
import a_clothes
import a_makeup
import a_random_item
import a_rhythm

def init():
    global image, buttons, score_font
    image = load_image('title.png')

    # 폰트 로드
    score_font = load_font('establish Retrosans.ttf', 24)

    # 버튼 위치 및 이미지 설정
    buttons = [
        {'name': 'Clothes', 'x': 450, 'y': 300, 'action': a_clothes},
        {'name': 'Makeup', 'x': 900, 'y': 300, 'action': a_makeup},
        {'name': 'Random Item', 'x': 1350, 'y': 300, 'action': a_random_item},
        {'name': 'Rhythm', 'x': 900, 'y': 150, 'action': a_rhythm}
    ]

def finish():
    global image
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            a_game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 900 - event.y
            for button in buttons:
                if button['x'] - 100 <= x <= button['x'] + 100 and button['y'] - 50 <= y <= button['y'] + 50:
                    a_game_framework.change_mode(button['action'])  # 버튼 클릭 시 모드 전환

def draw():
    clear_canvas()
    image.draw(900, 450)  # 타이틀 배경

    # 버튼 그리기
    for button in buttons:
        draw_rectangle(button['x'] - 100, button['y'] - 50, button['x'] + 100, button['y'] + 50)
        score_font.draw(button['x'] - 50, button['y'] - 12, button['name'], (255, 255, 255))  # 텍스트 추가

    update_canvas()

def update():
    pass
