from pico2d import *
import pygame
import random

# Pygame 초기화
pygame.init()

# Pico2D 초기화
open_canvas(800, 600)

# 게임 설정
line_y = 50  # 노트를 누르는 라인 위치
score = 0  # 점수
speed = 5  # 노트의 속도
notes = []  # 화면에 표시되는 노트 리스트

# 4개 영역 설정
key_zones = [
    {'key': SDLK_d, 'x': 150, 'width': 100},
    {'key': SDLK_f, 'x': 300, 'width': 100},
    {'key': SDLK_j, 'x': 500, 'width': 100},
    {'key': SDLK_k, 'x': 650, 'width': 100}
]

# Pygame 폰트 설정
pygame_font = pygame.font.Font(pygame.font.match_font('arial'), 36)
pygame_screen = pygame.display.set_mode((800, 600))  # Pygame 전용 화면

# 노트 클래스
class Note:
    def __init__(self, zone):
        self.zone = zone  # 노트가 속한 영역
        self.x = zone['x']
        self.y = 600  # 노트 생성 위치
        self.width = zone['width']
        self.height = 30

    def update(self):
        self.y -= speed  # 노트를 아래로 이동

    def draw(self):
        draw_rectangle(self.x - self.width // 2, self.y - self.height // 2,
                       self.x + self.width // 2, self.y + self.height // 2)


# 이벤트 처리 함수
def handle_events():
    global running, score

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

            # 키를 누르면 해당 구역의 노트와 충돌 판정
            for zone in key_zones:
                if event.key == zone['key']:
                    valid_notes = [note for note in notes if
                                   line_y - 15 <= note.y <= line_y + 15 and note.zone == zone]
                    if valid_notes:
                        notes.remove(valid_notes[0])  # 노트 제거
                        score += 1  # 점수 증가
                    else:
                        print("MISS")  # 단순한 MISS 출력


# Pygame 텍스트 렌더링 함수
def render_text_pygame(text, x, y, font, color=(255, 255, 255)):
    """Pygame의 텍스트를 화면에 그리기"""
    text_surface = font.render(text, True, color)
    pygame_screen.blit(text_surface, (x, y))


# 게임 루프
running = True

while running:
    clear_canvas()

    # 배경
    draw_rectangle(0, 0, 800, 600)

    # 영역 구분선
    for zone in key_zones:
        draw_rectangle(zone['x'] - zone['width'] // 2, 0,
                       zone['x'] + zone['width'] // 2, 600)

    # 랜덤 노트 생성
    if random.random() < 0.02:
        notes.append(Note(random.choice(key_zones)))

    # 노트 업데이트 및 그리기
    for note in notes:
        note.update()
        note.draw()

    # 노트가 화면을 벗어나면 MISS 처리
    notes = [note for note in notes if note.y >= 0]

    # Pygame 텍스트 렌더링
    pygame_screen.fill((0, 0, 0))  # Pygame 화면 초기화
    render_text_pygame(f"Score: {score}", 10, 10, pygame_font)

    # Pygame 화면 갱신
    pygame.display.flip()

    # 노트 누르는 라인
    draw_rectangle(0, line_y - 5, 800, line_y + 5)

    handle_events()
    update_canvas()
    delay(0.03)

close_canvas()
pygame.quit()
