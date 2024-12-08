from pico2d import *
import random
import time
import a_menu
import a_game_framework

class Ku:
    def __init__(self):
        self.x, self.y = 150, 300
        self.frame = 0
        self.dir = 0
        self.act = 0
        self.scale_factor = 5
        self.walk_image = load_image('pixilart-sprite.png')
        self.stop_image = load_image('stop.png')
        self.attack_image = load_image('Att.png')
        self.width = 100
        self.height = 100
        self.frame_delay = 0
        self.attacks = []
        self.is_attacking = False
        self.hp = 100
        self.font = load_font('establish Retrosans.ttf', 20)

    def update(self, monster):
        if not self.is_attacking:
            self.frame_delay += 1
            if self.frame_delay >= 10:
                self.frame = (self.frame + 1) % 4
                self.frame_delay = 0

        for attack in self.attacks[:]:
            attack.update()
            if collide(attack, monster):
                monster.monster_hp -= 30
                self.attacks.remove(attack)

        self.attacks = [attack for attack in self.attacks if attack.x < 1800]

        for monster_attack in monster.monster_attacks[:]:
            if collide(self, monster_attack):
                self.hp -= 30
                monster.monster_attacks.remove(monster_attack)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir = 1
                self.act = 1
            elif event.key == SDLK_SPACE:
                self.is_attacking = True
                self.attacks.append(Attack(self.x + 100, self.y))
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.dir = 0
                self.act = 0
            elif event.key == SDLK_SPACE:
                self.is_attacking = False

    def draw(self):
        scaled_width = self.width * self.scale_factor
        scaled_height = self.height * self.scale_factor
        if self.is_attacking:
            self.attack_image.draw(self.x, self.y, scaled_width, scaled_height)
        elif self.act == 0:
            self.stop_image.draw(self.x, self.y, scaled_width, scaled_height)
        else:
            self.walk_image.clip_draw(self.frame * self.width, 0, self.width, self.height,
                                      self.x, self.y, scaled_width, scaled_height)

        for attack in self.attacks:
            attack.draw()

        self.font.draw(self.x - 20, self.y + 200, f"HP: {self.hp}", (255, 0, 0))


class Attack:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('Att_ku.png')
        self.scale_factor = 8
        self.width = 50
        self.height = 50

    def update(self):
        self.x += 10

    def draw(self):
        scaled_width = self.width * self.scale_factor
        scaled_height = self.height * self.scale_factor
        self.image.draw(self.x, self.y, scaled_width, scaled_height)


class Background:
    def __init__(self):
        self.x = 0
        self.image = load_image('back_LL.png')
        self.width = 1800
        self.height = 900
        self.scroll_count = 0
        self.special_image = load_image('pixil-frame-0 2.png')
        self.special_image_visible = False
        self.special_y = 400
        self.special_image_meet = False
        self.monster_attacks = []
        self.last_attack_time = time.time()
        self.monster_hp = 120
        self.font = load_font('establish Retrosans.ttf', 20)

    def update(self, dir):
        if not self.special_image_meet:
            self.x -= dir * 2
            if self.x <= -self.width:
                self.x += self.width
                self.scroll_count += 1

            if self.scroll_count >= 5:
                self.special_image_visible = True

            if self.special_image_visible and self.special_y > 400:
                self.special_y -= 5
            elif self.special_image_visible and self.special_y <= 400:
                self.special_image_meet = True

        if self.special_image_meet:
            current_time = time.time()
            if current_time - self.last_attack_time >= 5:
                self.monster_attacks.append(MonsterAttack(1350, self.special_y))
                self.last_attack_time = current_time

        for attack in self.monster_attacks:
            attack.update()

        self.monster_attacks = [attack for attack in self.monster_attacks if attack.x > 0]

    def draw(self):
        self.image.draw(self.x + self.width // 2, self.height // 2, self.width, self.height)
        self.image.draw(self.x + self.width + self.width // 2, self.height // 2, self.width, self.height)

        if self.special_image_visible:
            scaled_width = 100 * 7
            scaled_height = 100 * 7
            self.special_image.draw(1350, self.special_y, scaled_width, scaled_height)
            self.font.draw(1350 - 30, self.special_y + 300, f"HP: {self.monster_hp}", (255, 0, 0))

        for attack in self.monster_attacks:
            attack.draw()


class MonsterAttack:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('Att_g.png')
        self.scale_factor = 8
        self.width = 50
        self.height = 50
        self.speed = random.randint(-10, -5)

    def update(self):
        self.x += self.speed

    def draw(self):
        scaled_width = self.width * self.scale_factor
        scaled_height = self.height * self.scale_factor
        self.image.draw(self.x, self.y, scaled_width, scaled_height)


def collide(a, b):
    if isinstance(b, Background):
        bx1, by1 = 1350 - 150, 400 - 150
        bx2, by2 = 1350 + 150, 400 + 150
    else:
        bx1, by1 = b.x - 50, b.y - 50
        bx2, by2 = b.x + 50, b.y + 50

    ax1, ay1 = a.x - 50, a.y - 50
    ax2, ay2 = a.x + 50, a.y + 50
    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)


def reset_world():
    global running, world, ku, background
    running = True
    world = []

    ku = Ku()
    background = Background()
    world.append(background)
    world.append(ku)


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
    if not background.special_image_meet:
        ku.update(background)
        background.update(ku.dir)
    else:
        ku.update(background)
        background.update(0)

    if ku.hp <= 0 or background.monster_hp <= 0:
        running = False
        show_result(ku.hp, background.monster_hp)


def draw():
    clear_canvas()
    for obj in world:
        obj.draw()
    update_canvas()


def show_result(ku_hp, monster_hp):
    clear_canvas()
    background.draw()  # 배경 유지
    ku.draw()  # 쿠 캐릭터 그리기
    for attack in ku.attacks:
        attack.draw()  # 쿠의 공격 그리기
    for monster_attack in background.monster_attacks:
        monster_attack.draw()  # 괴물의 공격 그리기

    # 결과 표시
    font = load_font('establish Retrosans.ttf', 60)
    if ku_hp <= 0:
        font.draw(700, 450, "LOSE", (255, 0, 0))
    elif monster_hp <= 0:
        font.draw(700, 450, "WIN", (0, 255, 0))

    # "메뉴로" 버튼 표시
    font = load_font('establish Retrosans.ttf', 40)
    font.draw(750, 150, "메뉴로", (255, 255, 255))
    draw_rectangle(700, 150, 900, 220)

    update_canvas()

    wait_for_menu_click()  # 메뉴로 이동 대기

# 예: 각 게임 모드의 finish() 함수
def finish():
    global ku, background, world

    # 존재하는지 확인한 후 삭제
    if 'ku' in globals():
        del ku
    if 'background' in globals():
        del background
    if 'world' in globals():
        del world


def wait_for_menu_click():
    """승패 화면에서 메뉴로 이동하기 위해 버튼 클릭 대기"""
    while True:
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                exit()
            elif event.type == SDL_MOUSEBUTTONDOWN:
                x, y = event.x, 900 - event.y
                if 700 <= x <= 900 and 150 <= y <= 220:  # "메뉴로" 버튼 클릭
                    a_game_framework.change_mode(a_menu)  # 메뉴로 전환
                    return
        delay(0.03)



def init():
    reset_world()
def update():
    """게임 루프에서 호출되는 업데이트 함수"""
    update_world()


def run():
    global running
    init()
    while running:
        handle_events()
        update_world()
        draw()
        delay(0.03)
    close_canvas()
