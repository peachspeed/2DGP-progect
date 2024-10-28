from pico2d import *
import random

# 캐릭터 주인공 쿠
class Ku:
    def __init__(self):
        self.x, self.y = 70, 150  # 500x500 화면 기준 오른쪽 밑
        self.frame = 0
        self.dir = 0
        self.action = 0
        self.act = 0  # 캐릭터의 동작 상태 (0 = 가만히, 1 = 걷기)
        self.walk_image = load_image('pixilart-sprite.png')
        self.stop_image = load_image('stop.png')

    def update(self):
        # 프레임을 계속 업데이트
        self.frame = (self.frame + 1) % 4

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir = 1  # 오른쪽 이동 시작
                self.act = 1  # 걷기 동작

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.dir = 0  # 이동 멈춤
                self.act = 0  # 가만히 있는 동작

    def draw(self):
        if self.act == 0:
            self.stop_image.draw(self.x, self.y, 230, 230)
        else:
            self.walk_image.clip_draw(self.frame * 100, 100 * self.action, 100, 100, self.x, self.y, 230, 230)


# 배경 클래스
class Background:
    def __init__(self):
        self.x = 0
        self.image = load_image('back_LL.png')

    def update(self, dir):
        # 캐릭터가 움직일 때 배경을 반대 방향으로 이동
        self.x -= dir * 5
        # 배경 이미지를 계속 반복해서 표시 (배경 초기화 조건 수정)
        if self.x <= -900:
            self.x += 900

    def draw(self):
        # 배경 이미지를 화면에 꽉 채워 표시하고 연속적으로 연결
        self.image.draw(self.x + 450, 350)  # 첫 번째 배경 (900x700 기준 중간)
        self.image.draw(self.x + 1350, 350)  # 이어지는 두 번째 배경


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            ku.handle_event(event)


def update_world():
    ku.update()
    background.update(ku.dir)  # 배경의 위치를 업데이트하여 캐릭터가 움직이는 효과 생성


def reset_world():
    global running
    global world
    global ku
    global background

    running = True
    world = []

    ku = Ku()
    background = Background()
    world.append(background)
    world.append(ku)


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas(900, 700)  # 캔버스를 배경 크기와 맞춤
reset_world()

# 게임 루프
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.15)

# 종료 코드
close_canvas()
