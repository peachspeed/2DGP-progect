from pico2d import *
import random

#캐릭터 주인공 쿠
class Ku:
    def __init__(self):
        self.x, self.y = 400, 150  # 캐릭터 위치
        self.frame = 0  # 현재 프레임
        self.dir = 0  # 방향 (0 = 가만히, 1 = 오른쪽)
        self.action = 0  # 캐릭터의 동작 상태 (0 = 가만히, 1 = 걷기)
        self.image = load_image('pixilart-sprite.png')  # 스프라이트 이미지 로드

    def update(self):
        # 가만히 있을 때도 프레임은 계속 업데이트됨
        self.frame = (self.frame + 1) % 4  # 프레임은 4개로 설정 (0, 1, 2, 3)

        # 방향에 따라 캐릭터의 위치를 업데이트
        if self.dir != 0:  # 오른쪽으로 이동할 때
            self.x += self.dir * 5  # x 좌표를 5만큼 이동 (속도 조정 가능)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                print("오른쪽 키 눌림")
                self.dir = 1  # 오른쪽 이동 시작
                self.action = 0

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                print("오른쪽 키에서 손 뗌")
                self.dir = 0  # 이동 멈춤
                self.action = 0  # 가만히 있는 동작 (action = 0)

    def draw(self):
        # 스프라이트 이미지에서 self.frame과 self.action에 맞는 프레임을 자르고 그립니다.
        self.image.clip_draw(self.frame * 100, 100 * self.action, 100, 100, self.x, self.y, 250, 250)


def menu():
    pass

def rhythm_game():
    pass

def RPG_confrontation():
    pass

def costume():
    pass

def makeup():
    pass

def random_ability():
    pass

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
    for o in world:
        o.update()
    pass


def reset_world():
    global running
    global grass
    global team
    global world
    global ku

    running = True
    world = []


    ku = Ku()
    world.append(ku)

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.25)
# finalization code
close_canvas()