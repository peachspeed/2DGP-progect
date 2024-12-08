import a_game_framework
import a_clothes
import a_makeup
import a_random_item
import a_rhythm
import a_2Dgame_step_1

from pico2d import *

# 일차를 추적하기 위한 변수
day = 1
MAX_DAYS = 7  # 게임의 최대 진행 일수

def init():
    global image, buttons, font
    image = load_image('menu.png')
    font = load_font('establish Retrosans.ttf', 40)  # 폰트 설정

    # 버튼 영역 설정 (각각의 x, y, width, height)
    buttons = [
        {'name': 'Clothes', 'x': 400, 'y': 550, 'width': 200, 'height': 100, 'action': a_clothes},
        {'name': 'Makeup', 'x': 400, 'y': 300, 'width': 200, 'height': 100, 'action': a_makeup},
        {'name': 'Random Item', 'x': 1350, 'y': 300, 'width': 200, 'height': 100, 'action': a_random_item},
        {'name': 'Rhythm', 'x': 400, 'y': 100, 'width': 200, 'height': 100, 'action': a_rhythm},
        {'name': '2D Game', 'x': 1350, 'y': 600, 'width': 200, 'height': 100, 'action': a_2Dgame_step_1}
    ]

def finish():
    global image, font
    del image, font

def handle_events():
    global day
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            a_game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 900 - event.y  # 마우스 좌표 변환
            for button in buttons:
                if (button['x'] - button['width'] // 2 <= x <= button['x'] + button['width'] // 2 and
                        button['y'] - button['height'] // 2 <= y <= button['y'] + button['height'] // 2):
                    if day <= MAX_DAYS:
                        a_game_framework.change_mode(button['action'])  # 클릭된 버튼의 모듈로 전환
                        day += 1  # 게임 실행 후 다음 날로 이동
                    return

            # "게임 끝" 버튼 클릭 처리
            if 700 <= x <= 900 and 200 <= y <= 260:
                a_game_framework.quit()

def draw():
    clear_canvas()
    image.draw(900, 450)  # 배경 이미지 그리기

    # 버튼 영역 표시 (예: 빨간 사각형)
    for button in buttons:
        draw_rectangle(button['x'] - button['width'] // 2, button['y'] - button['height'] // 2,
                       button['x'] + button['width'] // 2, button['y'] + button['height'] // 2)

    # 현재 일차 표시
    font.draw(800, 800, f"Day {day}", (0, 0, 0))  # 상단에 Day 표시

    # "게임 끝" 버튼 표시
    font.draw(50, 230, "게임 끝", (0, 0, 0))
    draw_rectangle(700, 200, 900, 260)  # "게임 끝" 버튼 클릭 영역

    # 게임 종료 메시지 표시
    if day > MAX_DAYS:
        font.draw(700, 600, "게임 완료! 더 이상 진행할 수 없습니다.", (0, 255, 0))

    update_canvas()

def update():
    pass
