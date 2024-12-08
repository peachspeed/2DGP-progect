from pico2d import *
import a_game_framework
import a_story2

def init():
    global image, font

    # 배경 이미지 로드
    image = load_image('story1.png')

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
                a_game_framework.change_mode(a_story2)

def draw():
    clear_canvas()

    # 배경 이미지 그리기
    image.draw(900, 450)

    # 텍스트 그리기
    font.draw(700, 800, "안녕 나는 쿠 라고 해.. ", (255, 255, 255))  # 흰색 텍스트
    font.draw(700, 700, "나는 평범한 마법소녀인데 오늘은 엄청 유명한 아이돌을 보러 왔어", (255, 255, 255))  # 흰색 텍스트

    update_canvas()

def update():
    pass
