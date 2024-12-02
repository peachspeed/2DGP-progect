from pico2d import *
import random

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600

# 각 아이템 확률 (희귀, 좋은, 일반, 쓰레기)
products = {
    'rare': 10,   # 희귀 아이템
    'good': 30,   # 좋은 아이템
    'normal': 45, # 일반 아이템
    'trash': 5    # 쓰레기 아이템
}

# 각 아이템 PNG 파일 목록
images = {
    'rare': ['rare1.png', 'rare2.png', 'rare3.png'],
    'good': ['good1.png', 'good2.png', 'good3.png'],
    'normal': ['normal1.png', 'normal2.png', 'normal3.png'],
    'trash': ['trash1.png', 'trash2.png', 'trash3.png']
}

# 뽑기 확률 계산
productrange = []
productresult = []

for product, chance in products.items():
    if not productrange:
        productrange.append(chance)
    else:
        productrange.append(productrange[-1] + chance)
    productresult.append(product)

def draw_image(image_file):
    """PNG 파일을 가운데에 그리는 함수"""
    img = load_image(image_file)
    img.draw(WIDTH // 2, HEIGHT // 2)

def pick_item():
    """랜덤 아이템을 뽑아 PNG 파일 반환"""
    tempresult = random.randint(1, productrange[-1])
    for i, range_value in enumerate(productrange):
        if tempresult <= range_value:
            category = productresult[i]
            return random.choice(images[category])  # 해당 카테고리에서 랜덤 파일 선택

def main():
    open_canvas(WIDTH, HEIGHT)
    background = load_image('Backcl.png')  # 배경 이미지 (없으면 생략 가능)
    button = load_image('button.png')     # 버튼 이미지
    current_image = None  # 현재 뽑힌 이미지

    button_width, button_height = button.w // 4, button.h // 4  # 버튼 크기 줄이기
    button_x, button_y = WIDTH // 2, 50  # 버튼 위치 아래로 100 이동

    click_count = 0  # 클릭 횟수
    max_clicks = 6   # 최대 클릭 횟수

    running = True
    while running:
        clear_canvas()
        background.draw(WIDTH // 2, HEIGHT // 2)  # 배경 그리기

        if current_image:
            draw_image(current_image)  # 현재 이미지가 있으면 화면에 그리기

        button.clip_draw(0, 0, button.w, button.h, button_x, button_y, button_width, button_height)  # 버튼 그리기

        update_canvas()

        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
            elif event.type == SDL_MOUSEBUTTONDOWN:
                x, y = event.x, HEIGHT - event.y
                if button_x - button_width // 2 <= x <= button_x + button_width // 2 and \
                   button_y - button_height // 2 <= y <= button_y + button_height // 2:
                    if click_count < max_clicks:
                        current_image = pick_item()  # 버튼 클릭 시 아이템 뽑기
                        click_count += 1
                        if click_count == max_clicks:
                            print("뽑기가 완료되었습니다. 프로그램을 종료합니다.")
                            running = False

    close_canvas()

if __name__ == '__main__':
    main()
