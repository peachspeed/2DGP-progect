from pico2d import *
import pygame
import random

# Pygame 초기화
pygame.init()

# Pico2D 초기화
open_canvas(1800, 900)

# 게임 설정
line_y = 150  # 노트를 누르는 라인 위치
score = 0  # 점수
speed = 5  # 노트의 속도
notes = []  # 화면에 표시되는 노트 리스트
game_started = False  # 게임 시작 여부
miss_active = False  # MISS 표시 활성화 여부
miss_timer = 0  # MISS 표시 시간 관리

# 4개 영역 설정
key_zones = [
    {'key': SDLK_d, 'x': 750, 'width': 100},
    {'key': SDLK_f, 'x': 850, 'width': 100},
    {'key': SDLK_j, 'x': 950, 'width': 100},
    {'key': SDLK_k, 'x': 1050, 'width': 100}
]

# 이미지 로드
background = load_image('backrythem.png')  # 배경 이미지
note_image = load_image('note.png')    # 노트 이미지
button_image = load_image('button.png')  # 시작 버튼 이미지
miss_image = load_image('miss.png')    # MISS 이미지

# 점수 폰트 로드
score_font = load_font('establish Retrosans.ttf', 60)


# 노트 클래스
class Note:
    def __init__(self, zone):
        self.zone = zone  # 노트가 속한 영역
        self.x = zone['x']
        self.y = 900  # 노트 생성 위치
        self.width = 100
        self.height = 30

    def update(self):
        self.y -= speed  # 노트를 아래로 이동

    def draw(self):
        note_image.draw(self.x, self.y)


def handle_events():
    """이벤트 처리 함수"""
    global running, game_started, score, miss_active, miss_timer

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            # 게임 시작 후 키 입력 처리
            if game_started:
                miss = True
                for zone in key_zones:
                    if event.key == zone['key']:
                        valid_notes = [note for note in notes if
                                       line_y - 15 <= note.y <= line_y + 15 and note.zone == zone]

                        if valid_notes:
                            notes.remove(valid_notes[0])  # 노트 제거
                            score += 1  # 점수 증가
                            miss = False
                if miss:
                    miss_active = True
                    miss_timer = get_time()
        elif event.type == SDL_MOUSEBUTTONDOWN and not game_started:
            # 시작 버튼 클릭 처리
            button_x, button_y = 1650, 150
            button_width, button_height = button_image.w // 4, button_image.h // 4
            x, y = event.x, 900 - event.y
            if (button_x - button_width // 2 <= x <= button_x + button_width // 2 and
                button_y - button_height // 2 <= y <= button_y + button_height // 2):
                game_started = True


def draw_zone():
    """영역 구분선 그리기"""
    for zone in key_zones:
        draw_rectangle(zone['x'] - zone['width'] // 2, 0,
                       zone['x'] + zone['width'] // 2, 900)


def draw_score_and_miss():
    """점수 및 MISS 이미지 표시"""
    # 점수 표시
    score_font.draw(200, 850, f"Score: {score}", (102, 178, 255))
    # MISS 표시
    if miss_active and get_time() - miss_timer < 1:  # MISS 표시 시간은 1초로 제한
        score_font.draw(1150, 850, f"miss", (255, 102, 178))

# 게임 루프
running = True

while running:
    clear_canvas()
    background.draw(900, 450)  # 배경 그리기

    if game_started:
        # 노트 누르는 라인
        draw_rectangle(0, line_y - 5, 1800, line_y + 5)

        # 영역 구분선 그리기
        draw_zone()

        # 점수 및 MISS 표시
        draw_score_and_miss()

        # 랜덤 노트 생성
        if random.random() < 0.02:
            notes.append(Note(random.choice(key_zones)))

        # 노트 업데이트 및 그리기
        for note in notes:
            note.update()
            note.draw()

        # 화면을 벗어난 노트 제거
        notes = [note for note in notes if note.y >= 0]
    else:
        # 시작 버튼 그리기
        button_image.clip_draw(0, 0, button_image.w, button_image.h, 1650, 150,
                               button_image.w // 4, button_image.h // 4)

    handle_events()
    update_canvas()
    delay(0.03)

close_canvas()
pygame.quit()
