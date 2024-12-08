from pico2d import *
import a_menu
import a_game_framework

# 전역 변수
running = True
dragging_item = None
background = None
ku = None
items = None
score_font = None  # 폰트 초기화
evaluation_result = ""  # 평가 결과
evaluation_active = False  # 평가 상태
menu_button_active = False  # 메뉴 버튼 활성화 상태

class DragItem:
    def __init__(self, x, y, image_path, item_type):
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.image = None  # 이미지는 나중에 로드
        self.image_path = image_path
        self.width, self.height = 1688, 2388
        self.resized_width = 400
        self.resized_height = int(self.height * (self.resized_width / self.width))
        self.dragging = False
        self.visible = True
        self.item_type = item_type  # 아이템 유형: 'hair', 'top', 'bottom'

    def load_image(self):
        self.image = load_image(self.image_path)

    def draw(self):
        if self.visible and self.image:
            self.image.draw(self.x, self.y, self.resized_width, self.resized_height)

    def is_inside(self, x, y):
        x1, y1, x2, y2 = self.get_collision_box()
        return x1 <= x <= x2 and y1 <= y <= y2

    def get_collision_box(self):
        collision_width = 100
        if self.item_type == 'hair':
            collision_height = 100
            y_offset = 200
        elif self.item_type == 'top':
            collision_height = 200
            y_offset = 100
        elif self.item_type == 'bottom':
            collision_height = 300
            y_offset = -70
        else:
            collision_height = 100
            y_offset = 0

        x1 = self.x - collision_width // 2
        y1 = self.y + y_offset - collision_height // 2
        x2 = self.x + collision_width // 2
        y2 = self.y + y_offset + collision_height // 2
        return x1, y1, x2, y2

    def set_position(self, x, y):
        self.x, self.y = x, y

    def reset_position(self):
        self.x, self.y = self.original_x, self.original_y


class Ku:
    def __init__(self):
        self.x, self.y = 300, 450  # 중앙에 위치
        self.image = None
        self.width = 1688
        self.height = 2388
        self.scale_factor = 2.5
        self.resized_width = int(300 * self.scale_factor)
        self.resized_height = int(self.height * (self.resized_width / self.width))
        self.worn_items = []

    def load_image(self):
        self.image = load_image('ku.png')

    def draw(self):
        if self.image:
            self.image.draw(self.x, self.y, self.resized_width, self.resized_height)
        for item in self.worn_items:
            item.image.draw(self.x, self.y, self.resized_width, self.resized_height)

    def get_worn_items(self):
        return {item.item_type: item.image_path for item in self.worn_items}

    def wear_item(self, item):
        # 동일 타입의 기존 아이템 제거
        for worn_item in self.worn_items:
            if worn_item.item_type == item.item_type:
                worn_item.visible = True
                worn_item.reset_position()
                self.worn_items.remove(worn_item)
                break
        # 새로운 아이템 착용
        self.worn_items.append(item)
        item.visible = False


class Background:
    def __init__(self):
        self.image = None

    def load_image(self):
        self.image = load_image('Backcl.png')

    def draw(self):
        if self.image:
            self.image.draw(900, 450)


def reset_world():
    global running, ku, background, items, dragging_item

    running = True
    dragging_item = None

    ku = Ku()
    background = Background()

    # 의상 및 액세서리 생성
    items = (
        [DragItem(700 + (i % 7) * 150, 600 - (i // 7) * 150, f'hair{i}.png', 'hair') for i in range(1, 15)] +
        [DragItem(700 + (i % 7) * 150, 450 - (i // 7) * 150, f'top{i}.png', 'top') for i in range(1, 9)] +
        [DragItem(700 + (i % 7) * 150, 300 - (i // 7) * 150, f'bottom{i}.png', 'bottom') for i in range(1, 8)]
    )


def init():
    global ku, background, items, score_font, evaluation_font
    reset_world()

    ku.load_image()
    background.load_image()
    for item in items:
        item.load_image()

    # 폰트 로드
    score_font = load_font('establish Retrosans.ttf', 30)
    evaluation_font = load_font('establish Retrosans.ttf', 70)  # 평가용 큰 폰트





def evaluate_fashion():
    """패션 평가"""
    global evaluation_result, evaluation_active, menu_button_active
    worn_items = ku.get_worn_items()
    hair = worn_items.get('hair', '')
    top = worn_items.get('top', '')
    bottom = worn_items.get('bottom', '')

    if (hair == 'hair14.png' and top == 'top8.png' and bottom == 'bottom7.png') or \
       (hair == 'hair13.png' and top == 'top7.png' and bottom == 'bottom6.png'):
        evaluation_result = "최고의 옷!"
    elif (top == 'top3.png' and bottom == 'bottom2.png') or \
         (top == 'top4.png' and bottom == 'bottom5.png'):
        evaluation_result = "최악의 옷..."
    else:
        evaluation_result = "낫 배드!"

    evaluation_active = True
    menu_button_active = True


def handle_events():
    global running, dragging_item, evaluation_active
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 900 - event.y
            if evaluation_active:
                if 1600 <= x <= 1700 and 50 <= y <= 100:  # "메뉴로" 버튼 클릭
                    a_game_framework.change_mode(a_menu)
            else:
                for item in items:
                    if item.is_inside(x, y) and item.visible:
                        dragging_item = item
                        dragging_item.dragging = True
                        break
                if 50 <= x <= 150 and 50 <= y <= 100:  # "완성" 버튼 클릭
                    evaluate_fashion()
        elif event.type == SDL_MOUSEMOTION:
            if dragging_item and dragging_item.dragging:
                dragging_item.set_position(event.x, 900 - event.y)
        elif event.type == SDL_MOUSEBUTTONUP:
            if dragging_item:
                ku.wear_item(dragging_item)
                dragging_item.dragging = False
                dragging_item = None


def draw():
    clear_canvas()
    background.draw()
    ku.draw()
    for item in items:
        item.draw()
    # "완성" 버튼
    draw_rectangle(50, 50, 150, 100)
    score_font.draw(60, 60, "완성", (0, 0, 0))

    if evaluation_active:
        # 평가 결과
        evaluation_font.draw(900, 450, evaluation_result, (0, 0, 255))  # 파란색 글씨
        # "메뉴로" 버튼
        draw_rectangle(1600, 50, 1700, 100)
        score_font.draw(1610, 60, "메뉴로", (0, 0, 0))

    update_canvas()
# 예: 각 게임 모드의 finish() 함수
def finish():
    global background, ku, items, score_font

    # 삭제 전에 존재 여부 확인
    if 'background' in globals():
        del background
    if 'ku' in globals():
        del ku
    if 'items' in globals():
        del items
    if 'score_font' in globals():
        del score_font

def update():
    pass


def run():
    init()
    while running:
        handle_events()
        draw()
        update()
        delay(0.03)
    finish()
