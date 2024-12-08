from pico2d import *
import a_game_framework
import a_menu
import random

# 전역 변수
line_y = 150
score = 0
speed = 0.3
notes = []
game_started = False
miss_active = False
miss_timer = 0
miss_count = 0
start_time = None
game_over = False
end_message = ""
running = True

button_width, button_height = 500, 200
note_width, note_height = 100, 30

# 이미지 로드
def load_resources():
    global background, note_image, button_image, score_font
    try:
        background = load_image('backrythem.png')
        note_image = load_image('note.png')
        button_image = load_image('button.png')
        score_font = load_font('establish Retrosans.ttf', 60)
    except Exception as e:
        print(f"Error loading resources: {e}")
        exit()

# 키 입력 영역
key_zones = [
    {'key': SDLK_d, 'x': 750, 'width': 100},
    {'key': SDLK_f, 'x': 850, 'width': 100},
    {'key': SDLK_j, 'x': 950, 'width': 100},
    {'key': SDLK_k, 'x': 1050, 'width': 100}
]

class Note:
    def __init__(self, zone):
        self.zone = zone
        self.x = zone['x']
        self.y = 900
        self.width = note_width
        self.height = note_height

    def update(self):
        self.y -= speed

    def draw(self):
        note_image.draw(self.x, self.y, self.width, self.height)

# 초기화
def init():
    global score, speed, notes, game_started, miss_active, miss_timer, miss_count, start_time, game_over, end_message
    load_resources()
    score = 0
    speed = 0.3
    notes = []
    game_started = False
    miss_active = False
    miss_timer = 0
    miss_count = 0
    start_time = None
    game_over = False
    end_message = ""

# 종료 함수 (필수 추가)


# 이벤트 처리
def handle_events():
    global running, game_started, score, miss_active, miss_timer, miss_count, game_over, end_message, start_time
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            if game_started and not game_over:
                miss = True
                for zone in key_zones:
                    if event.key == zone['key']:
                        valid_notes = [note for note in notes if
                                       line_y - 15 <= note.y <= line_y + 15 and note.zone == zone]
                        if valid_notes:
                            notes.remove(valid_notes[0])
                            score += 1
                            miss = False
                if miss:
                    miss_active = True
                    miss_timer = get_time()
                    miss_count += 1
                    if miss_count >= 10:
                        game_over = True
                        end_message = "MISS 10개"
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 900 - event.y
            if not game_started:
                button_x, button_y = 1650, 150
                if (button_x - button_width // 2 <= x <= button_x + button_width // 2 and
                        button_y - button_height // 2 <= y <= button_y + button_height // 2):
                    game_started = True
                    start_time = get_time()
                    print("게임 시작!")
            elif game_over:
                menu_button_x, menu_button_y = 1500, 50
                menu_button_width, menu_button_height = 200, 50
                if (menu_button_x - menu_button_width // 2 <= x <= menu_button_x + menu_button_width // 2 and
                        menu_button_y - menu_button_height // 2 <= y <= menu_button_y + menu_button_height // 2):
                    a_game_framework.change_mode(a_menu)

# 상태 업데이트
def update():
    global game_over, end_message, speed, notes
    if game_started and not game_over:
        elapsed_time = get_time() - start_time
        if elapsed_time >= 60:
            game_over = True
            end_message = "끝"
        else:
            speed = 0.3 + (elapsed_time / 60) * 2

        if random.random() < 0.005:
            notes.append(Note(random.choice(key_zones)))

        for note in notes:
            note.update()

        notes = [note for note in notes if note.y >= 0]

def update_miss():
    global miss_active
    if miss_active and get_time() - miss_timer > 1:
        miss_active = False

# 화면 그리기
def draw():
    clear_canvas()
    background.draw(900, 450)
    if game_started:
        if not game_over:
            draw_rectangle(0, line_y - 5, 1800, line_y + 5)
            for note in notes:
                note.draw()
            score_font.draw(200, 850, f"Score: {score}", (102, 178, 255))
            if miss_active:
                score_font.draw(1150, 850, f"MISS", (255, 102, 178))
        else:
            score_font.draw(900, 450, end_message, (255, 0, 0))
            draw_rectangle(1500 - 100, 50 - 25, 1500 + 100, 50 + 25)
            score_font.draw(1400, 40, "메뉴로", (0, 0, 0))
    else:
        button_image.clip_draw(0, 0, button_image.w, button_image.h, 1650, 150,
                               button_width // 4, button_height // 4)
    update_canvas()
# 예: 각 게임 모드의 finish() 함수
def finish():
    global background, note_image, button_image, score_font

    # 변수 존재 여부를 확인한 후 삭제
    if 'background' in globals():
        del background
    if 'note_image' in globals():
        del note_image
    if 'button_image' in globals():
        del button_image
    if 'score_font' in globals():
        del score_font


# 게임 실행
def run():
    global running
    init()
    while running:
        draw()
        handle_events()
        update()
        update_miss()
        delay(0.03)
