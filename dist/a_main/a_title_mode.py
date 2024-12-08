import a_game_framework
import a_story1
import a_rhythm
from pico2d import *

def init():
    global image, font

    # 배경 이미지 로드
    image = load_image('title.png')

    # 폰트 로드
    font = load_font('establish Retrosans.ttf', 30)  # 폰트 크기 30으로 설정

def finish():
    global image, font

    # 리소스 해제
    del image, font

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            a_game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                a_game_framework.change_mode(a_story1)  # 스페이스바로 스토리1 이동
def draw():
    clear_canvas()

    # 배경 이미지 그리기
    image.draw(900, 450)

    # 폰트로 텍스트 표시
    font.draw(600, 200, "Press SPACE to Start Story", (255, 255, 255))  # 스토리 시작

    update_canvas()

def update():
    pass
