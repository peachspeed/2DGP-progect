from pico2d import *

class DragItem:
    def __init__(self, x, y, image_path, item_type):
        self.x = x
        self.y = y
        self.original_x = x  # 원래 위치 저장
        self.original_y = y
        self.image = load_image(image_path)
        self.width, self.height = 1688, 2388
        self.resized_width = 400  # 크기를 2배로 확대
        self.resized_height = int(self.height * (self.resized_width / self.width))
        self.dragging = False
        self.visible = True  # 아이템이 보이는지 여부
        self.item_type = item_type  # 아이템 유형: 'hair', 'top', 'bottom'

    def draw(self):
        if self.visible:  # 아이템이 보이는 경우만 그리기
            self.image.draw(self.x, self.y, self.resized_width, self.resized_height)
            # 충돌 구간 표시
            x1, y1, x2, y2 = self.get_collision_box()
            draw_rectangle(x1, y1, x2, y2)

    def is_inside(self, x, y):
        """충돌 구간 확인"""
        x1, y1, x2, y2 = self.get_collision_box()
        return x1 <= x <= x2 and y1 <= y <= y2

    def get_collision_box(self):
        """아이템 충돌 영역 반환"""
        collision_width = 100  # 가로 충돌 크기 일정

        # 위치에 따라 충돌 영역의 중심을 조정
        if self.item_type == 'hair':
            collision_height = 100
            y_offset = 200  # 위로 200 이동
        elif self.item_type == 'top':
            collision_height = 200
            y_offset = 100  # 위로 100 이동
        elif self.item_type == 'bottom':
            collision_height = 300
            y_offset = -70  # 아래로 100 이동
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
        """원래 위치로 돌아가기"""
        self.x, self.y = self.original_x + 100, self.original_y + 100

class Ku:
    def __init__(self):
        self.x, self.y = 350, 450  # 왼쪽 중앙에 위치
        self.image = load_image('ku.png')
        self.width = 1688
        self.height = 2388
        self.scale_factor = 2.5  # 크기 조정 비율
        self.resized_width = int(300 * self.scale_factor)
        self.resized_height = int(self.height * (self.resized_width / self.width))
        self.worn_items = []  # 착용 중인 아이템 리스트

    def draw(self):
        # 기본 캐릭터 그리기
        self.image.draw(self.x, self.y, self.resized_width, self.resized_height)
        # 착용 중인 아이템 그리기 (나중에 입힌 아이템이 위로 오도록)
        for item in self.worn_items:
            item.image.draw(self.x, self.y, self.resized_width, self.resized_height)

        # 좁혀진 범위 빨간 테두리로 표시
        x1, y1, x2, y2 = self.get_collision_box()
        draw_rectangle(x1, y1, x2, y2)

    def get_collision_box(self):
        """좁혀진 범위를 반환 (가로 세로 각 100씩 좁힘)"""
        x1 = self.x - (self.resized_width // 2 - 170)
        y1 = self.y - (self.resized_height // 2 - 100)
        x2 = self.x + (self.resized_width // 2 - 200)
        y2 = self.y + (self.resized_height // 2 - 100)
        return x1, y1, x2, y2

    def is_inside(self, item):
        """아이템이 Ku의 좁혀진 범위 안에 있는지 확인"""
        x1, y1, x2, y2 = self.get_collision_box()
        return x1 < item.x < x2 and y1 < item.y < y2

    def wear_item(self, item):
        # 동일 타입 아이템이 이미 착용 중이면 벗기기
        for worn_item in self.worn_items:
            if worn_item.item_type == item.item_type:
                worn_item.visible = True
                worn_item.reset_position()
                self.worn_items.remove(worn_item)
                break
        # 새 아이템 착용 (맨 앞으로 추가)
        self.worn_items.append(item)
        item.visible = False

    def remove_item(self, x, y):
        # 착용 중인 아이템을 클릭하면 분리
        for item in self.worn_items:
            if item.is_inside(x, y):  # 아이템 클릭 범위 확인
                item.visible = True  # 아이템 다시 보이게 설정
                item.reset_position()  # 초기 위치로 이동
                self.worn_items.remove(item)
                return item
        return None

# 배경 클래스
class Background:
    def __init__(self):
        self.image = load_image('Backcl.png')  # 배경 이미지 로드
        self.original_width = 2400
        self.original_height = 1200
        self.resized_width = 1800  # 원하는 크기로 줄이기
        self.resized_height = 900

    def draw(self):
        # 배경을 clip_draw로 중앙에 표시
        self.image.clip_draw(
            0, 0, self.original_width, self.original_height,  # 원본 이미지 전체를 자름
            900, 450, self.resized_width, self.resized_height  # 조정된 크기로 캔버스 중앙에 그림
        )


def handle_events():
    global running, dragging_item

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 900 - event.y  # 마우스 좌표 변환
            # Ku 캐릭터에서 착용된 아이템 분리
            dragging_item = ku.remove_item(x, y)
            if dragging_item:
                dragging_item.dragging = True
                continue  # Ku에서 아이템 분리되면 아래는 실행 안 함
            # 오른쪽 아이템 드래그 시작
            for item in items:
                if item.is_inside(x, y) and item.visible:  # 보이는 아이템만 클릭 가능
                    dragging_item = item
                    dragging_item.dragging = True
                    break
        elif event.type == SDL_MOUSEMOTION:
            if dragging_item and dragging_item.dragging:
                dragging_item.set_position(event.x, 900 - event.y)
        elif event.type == SDL_MOUSEBUTTONUP:
            if dragging_item:
                if ku.is_inside(dragging_item):
                    ku.wear_item(dragging_item)  # 아이템 착용
                dragging_item.dragging = False
                dragging_item = None


def reset_world():
    global running, ku, background, items, dragging_item

    running = True
    dragging_item = None

    ku = Ku()
    background = Background()

    # 의상 및 액세서리 생성: 머리카락 -> 상의 -> 바지 순서로 정렬
    items = (
        [DragItem(0, 0, f'hair{i}.png', 'hair') for i in range(1, 15)] +  # 머리카락
        [DragItem(0, 0, f'top{i}.png', 'top') for i in range(1, 9)] +    # 상의
        [DragItem(0, 0, f'bottom{i}.png', 'bottom') for i in range(1, 8)]  # 바지
    )

    # 위치 정렬: 가로 7개씩 배치, 세로 7줄로 조정
    x_start = 700  # 시작 x 좌표 (약간 왼쪽으로 조정)
    y_start = 900  # 시작 y 좌표
    x_spacing = 150  # 가로 간격
    y_spacing = 150  # 세로 간격

    for i, item in enumerate(items):
        item.x = x_start + (i % 7) * x_spacing  # 가로로 7개씩 배치
        item.y = y_start - (i // 7) * y_spacing  # 새 줄마다 y 감소

        # 머리카락 아이템은 y 위치를 200만큼 아래로 조정
        if item.item_type == 'hair':
            item.y -= 250
        if item.item_type == 'top':
            item.y -= 150
        if item.item_type == 'bottom':
            item.y -=100




def render_world():
    clear_canvas()
    background.draw()
    ku.draw()
    for item in items:
        item.draw()
    update_canvas()


# 메인 실행
open_canvas(1800, 900)  # 캔버스 크기 설정
reset_world()

while running:
    handle_events()
    render_world()
    delay(0.03)

close_canvas()

