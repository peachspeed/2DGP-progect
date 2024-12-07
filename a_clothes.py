from pico2d import *

# 전역 변수
running = True
dragging_item = None
background = None
ku = None
items = None

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

    def get_collision_box(self):
        """좁혀진 충돌 범위 반환"""
        x1 = self.x - (self.resized_width // 2 - 150)
        y1 = self.y - (self.resized_height // 2 - 200)
        x2 = self.x + (self.resized_width // 2 - 150)
        y2 = self.y + (self.resized_height // 2 - 200)
        return x1, y1, x2, y2

    def is_inside(self, item):
        """아이템이 충돌 범위 안에 있는지 확인"""
        x1, y1, x2, y2 = self.get_collision_box()
        return x1 <= item.x <= x2 and y1 <= item.y <= y2

    def wear_item(self, item):
        """아이템을 착용"""
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
    global ku, background, items
    reset_world()

    ku.load_image()
    background.load_image()
    for item in items:
        item.load_image()


def finish():
    global background, ku, items
    del background, ku, items


def handle_events():
    global running, dragging_item
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 900 - event.y
            for item in items:
                if item.is_inside(x, y) and item.visible:
                    dragging_item = item
                    dragging_item.dragging = True
                    break
        elif event.type == SDL_MOUSEMOTION:
            if dragging_item and dragging_item.dragging:
                dragging_item.set_position(event.x, 900 - event.y)
        elif event.type == SDL_MOUSEBUTTONUP:
            if dragging_item:
                if ku.is_inside(dragging_item):  # 충돌 확인
                    ku.wear_item(dragging_item)  # 아이템 착용
                dragging_item.dragging = False
                dragging_item = None



def update():
    pass


def draw():
    clear_canvas()
    background.draw()
    ku.draw()
    for item in items:
        item.draw()
    update_canvas()


def run():
    init()
    while running:
        handle_events()
        draw()
        delay(0.03)
    finish()
