from pico2d import *

# 전역 변수 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 1800, 900
face_back = None  # 배경 이미지
face = None       # 얼굴 이미지
buttons = []
current_makeup = None

# 버튼 클래스 정의
class Button:
    def __init__(self, x, y, image_path, makeup_path, scale=0.5):  # scale=0.4로 기본값 설정
        self.image = load_image(image_path)
        self.makeup = load_image(makeup_path)
        self.x, self.y = x, y
        self.scale = scale  # 스케일 값 저장

    def draw(self):
        # 이미지 크기를 조정하여 그리기
        width = int(self.image.w * self.scale)  # 스케일 적용
        height = int(self.image.h * self.scale)  # 스케일 적용
        self.image.clip_draw(0, 0, self.image.w, self.image.h, self.x, self.y, width, height)

        # 클릭 가능한 범위를 빨간색 네모로 표시
        draw_rectangle(self.x - width // 2, self.y - height // 2,
                       self.x + width // 2, self.y + height // 2)

    def is_clicked(self, x, y):
        # 버튼 클릭 확인 (스케일 적용)
        width = int(self.image.w * self.scale)
        height = int(self.image.h * self.scale)
        if self.x - width // 2 <= x <= self.x + width // 2 and \
           self.y - height // 2 <= y <= self.y + height // 2:
            return True
        return False

def enter():
    global face_back, face, buttons
    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    face_back = load_image('face back.png')  # 배경으로 사용할 이미지
    face = load_image('face back.png')  # 중앙의 얼굴 이미지

    # 버튼 및 화장 이미지 설정
    colors = ['orange', 'purple', 'brown', 'blue', 'pink', 'green']
    for i, color in enumerate(colors):
        button_x = SCREEN_WIDTH - 100  # 버튼은 오른쪽 끝에 위치
        button_y = SCREEN_HEIGHT + 70 - (i + 1) * 150  # 버튼 간격 유지 + 50 위로 이동
        button = Button(button_x, button_y, f'{color}.png', f'makeup_{color}.png', scale=0.5)
        buttons.append(button)

def update():
    pass
def draw():
    global current_makeup
    clear_canvas()
    face_back.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # 배경을 화면 전체에 채움

    # 얼굴 그리기
    face.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # 얼굴을 캔버스 정중앙에 배치

    # 현재 선택된 화장 그리기
    if current_makeup:
        current_makeup.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # 버튼 그리기
    for button in buttons:
        button.draw()
    update_canvas()

def handle_events():
    global current_makeup
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            close_canvas()
            exit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            x, y = event.x, SCREEN_HEIGHT - event.y  # Y좌표 변환
            for button in buttons:
                if button.is_clicked(x, y):
                    current_makeup = button.makeup  # 선택된 화장 이미지 설정

def main():
    enter()
    while True:
        handle_events()
        update()
        draw()

if __name__ == '__main__':
    main()
