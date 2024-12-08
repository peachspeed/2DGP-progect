from pico2d import *
from pygame.draw_py import draw_line

import a_menu
import a_game_framework


def init():
    global face_back, face, buttons, current_makeup, menu_button
    face_back = load_image('face back.png')  # 배경 이미지
    face = load_image('face back.png')  # 얼굴 이미지
    current_makeup = None

    # 버튼 설정 (간격을 130으로 조정, 크기를 100으로 확대)
    colors = ['orange', 'purple', 'brown', 'blue', 'pink', 'green']
    buttons = [
        {'color': color, 'image': load_image(f'{color}.png'), 'makeup': load_image(f'makeup_{color}.png'),
         'x': 1700, 'y': 800 - i * 130, 'width': 100, 'height': 100}  # 크기를 100으로 확장, 간격을 130으로 조정
        for i, color in enumerate(colors)
    ]

    # "메뉴로" 버튼 설정
    menu_button = {'x': 1600, 'y': 50, 'width': 150, 'height': 50}  # "메뉴로" 버튼 위치와 크기 설정

# 예: 각 게임 모드의 finish() 함수
def finish():
    global face_back, face, buttons, current_makeup, menu_button

        # 삭제 전에 존재 여부 확인
    if 'face_back' in globals():
            del face_back
    if 'face' in globals():
            del face
    if 'buttons' in globals():
            del buttons
    if 'current_makeup' in globals():
            del current_makeup
    if 'menu_button' in globals():
            del menu_button


def handle_events():
    global current_makeup
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 900 - event.y
            # 버튼 클릭 처리
            for button in buttons:
                if (button['x'] - button['width'] // 2 <= x <= button['x'] + button['width'] // 2 and
                        button['y'] - button['height'] // 2 <= y <= button['y'] + button['height'] // 2):
                    current_makeup = button['makeup']

            # "메뉴로" 버튼 클릭 처리
            if (menu_button['x'] - menu_button['width'] // 2 <= x <= menu_button['x'] + menu_button['width'] // 2 and
                    menu_button['y'] - menu_button['height'] // 2 <= y <= menu_button['y'] + menu_button['height'] // 2):
                a_game_framework.change_mode(a_menu)  # 메뉴로 전환


def draw():
    clear_canvas()
    face_back.draw(900, 450)
    face.draw(900, 450)
    if current_makeup:
        current_makeup.draw(900, 450)

    # 버튼 그리기 및 클릭 가능한 영역 표시
    for button in buttons:
        button['image'].draw(button['x'], button['y'], button['width'], button['height'])  # 크기를 100으로 확대
        draw_rectangle(button['x'] - button['width'] // 2, button['y'] - button['height'] // 2,
                       button['x'] + button['width'] // 2, button['y'] + button['height'] // 2)  # 클릭 범위 표시

    # "메뉴로" 버튼 그리기 및 클릭 가능한 영역 표시
    draw_rectangle(menu_button['x'] - menu_button['width'] // 2, menu_button['y'] - menu_button['height'] // 2,
                   menu_button['x'] + menu_button['width'] // 2, menu_button['y'] + menu_button['height'] // 2)
    font = load_font('establish Retrosans.ttf', 30)
    font.draw(menu_button['x'] - 60, menu_button['y'] - 10, "메뉴로", (0, 0, 0))

    update_canvas()



def update():
    pass
