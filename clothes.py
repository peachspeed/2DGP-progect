from pico2d import *

# 옷/머리 액세서리 클래스
class DragItem:
    def __init__(self, x, y, image_path, item_type):
        self.x = x
        self.y = y
        self.image = load_image(image_path)
        self.width, self.height = 1688, 2388
        self.resized_width = 200  # 화면에 맞게 조정한 크기
        self.resized_height = int(self.height * (self.resized_width / self.width))
        self.dragging = False
        self.item_type = item_type  # 아이템 유형: 'hair', 'top', 'bottom'

    def draw(self):
        self.image.draw(self.x, self.y, self.resized_width, self.resized_height)

    def is_inside(self, x, y):
        # 아이템 유형에 따라 클릭 가능한 영역을 다르게 설정
        if self.item_type == 'hair':  # 헤어: 윗부분만 클릭 가능
            return self.x - self.resized_width // 2 < x < self.x + self.resized_width // 2 and \
                   self.y + self.resized_height // 4 < y < self.y + self.resized_height // 2
        elif self.item_type == 'top':  # 상의: 가운데 부분만 클릭 가능
            return self.x - self.resized_width // 2 < x < self.x + self.resized_width // 2 and \
                   self.y - self.resized_height // 4 < y < self.y + self.resized_height // 4
        elif self.item_type == 'bottom':  # 하의: 아랫부분만 클릭 가능
            return self.x - self.resized_width // 2 < x < self.x + self.resized_width // 2 and \
                   self.y - self.resized_height // 2 < y < self.y - self.resized_height // 4
        return False

    def set_position(self, x, y):
        self.x, self.y = x, y


# 캐릭터 주인공 Ku
class Ku:
    def __init__(self):
        self.x, self.y = 200, 350  # 왼쪽 중앙에 위치
        self.image = load_image('ku.png')
        self.width = 1688
        self.height = 2388
        self.resized_width = 300
        self.resized_height = int(self.height * (self.resized_width / self.width))
        self.worn_items = []  # 착용 중인 아이템 리스트

    def draw(self):
        # 기본 캐릭터 그리기
        self.image.draw(self.x, self.y, self.resized_width, self.resized_height)
        # 착용 중인 아이템 그리기
        for item in self.worn_items:
            item.image.draw(self.x, self.y, self.resized_width, self.resized_height)

    def wear_item(self, item):
        # 아이템을 착용 목록에 추가
        if item not in self.worn_items:
            self.worn_items.append(item)

    def remove_item(self, item):
        # 아이템을 착용 목록에서 제거
        if item in self.worn_items:
            self.worn_items.remove(item)

    def is_inside(self, item):
        # 아이템이 Ku의 범위 안에 있는지 확인
        return self.x - self.resized_width // 2 < item.x < self.x + self.resized_width // 2 and \
               self.y - self.resized_height // 2 < item.y < self.y + self.resized_height // 2


# 배경 클래스
class Background:
    def __init__(self):
        self.image = load_image('back_LL.png')

    def draw(self):
        self.image.draw(450, 350)  # 배경을 화면 중앙에 표시


def handle_events():
    global running, dragging_item

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 700 - event.y  # 마우스 좌표 변환
            for item in items:
                if item.is_inside(x, y):
                    dragging_item = item
                    dragging_item.dragging = True
                    break
        elif event.type == SDL_MOUSEMOTION:
            if dragging_item and dragging_item.dragging:
                dragging_item.set_position(event.x, 700 - event.y)
        elif event.type == SDL_MOUSEBUTTONUP:
            if dragging_item:
                if ku.is_inside(dragging_item):
                    ku.wear_item(dragging_item)  # 아이템 착용
                else:
                    ku.remove_item(dragging_item)  # 아이템 벗기기
                dragging_item.dragging = False
                dragging_item = None


# 초기화 함수
def reset_world():
    global running, ku, background, items, dragging_item

    running = True
    dragging_item = None

    ku = Ku()
    background = Background()

    # 의상 및 액세서리 생성
    items = [
        DragItem(750, 600, 'top1.png', 'top'),
        DragItem(850, 600, 'top2.png', 'top'),
        DragItem(750, 500, 'top3.png', 'top'),
        DragItem(850, 500, 'top4.png', 'top'),
        DragItem(750, 400, 'bottom1.png', 'bottom'),
        DragItem(850, 400, 'bottom2.png', 'bottom'),
        DragItem(750, 300, 'bottom3.png', 'bottom'),
        DragItem(850, 300, 'hair1.png', 'hair'),
        DragItem(750, 200, 'hair2.png', 'hair'),
        DragItem(850, 200, 'hair3.png', 'hair'),
        DragItem(750, 100, 'hair4.png', 'hair'),
        DragItem(850, 100, 'hair5.png', 'hair'),
        DragItem(750, 50, 'hair6.png', 'hair'),
        DragItem(850, 50, 'hair7.png', 'hair')
    ]


def render_world():
    clear_canvas()
    background.draw()
    ku.draw()
    for item in items:
        item.draw()
    update_canvas()


# 메인 실행
open_canvas(900, 700)  # 캔버스 크기 설정
reset_world()

while running:
    handle_events()
    render_world()
    delay(0.03)

close_canvas()
