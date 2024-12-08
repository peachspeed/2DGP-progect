from pico2d import *
import a_game_framework
import a_story3

def init():
    global image, bgm, font

    # 배경 이미지 로드
    image = load_image('story2.png')

    # 배경 음악 로드 및 재생
    bgm = load_music('3-cream-soda-cute-bgm-271159.mp3')  # 원하는 음악 파일 경로
    bgm.set_volume(64)  # 음악 볼륨 설정 (0~128)
    bgm.repeat_play()  # 음악 반복 재생

    # 폰트 로드
    font = load_font('establish Retrosans.ttf', 30)  # 폰트 크기 30으로 설정

def finish():
    global image, bgm, font

    # 리소스 해제
    del image, bgm, font

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            a_game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                a_game_framework.change_mode(a_story3)

def draw():
    clear_canvas()

    # 배경 이미지 그리기
    image.draw(900, 450)

    # 텍스트 그리기
    font.draw(500, 700, "와아아ㅏ!!!!", (255, 255, 255))  # 흰색 텍스트

    update_canvas()

def update():
    pass
