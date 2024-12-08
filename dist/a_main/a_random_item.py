from pico2d import *
import random
import a_menu
import a_game_framework

def init():
    global background, button, current_image, click_count, max_clicks, item_images, used_items, menu_button_active
    background = load_image('Backcl.png')
    button = load_image('button.png')
    current_image = None
    click_count = 0
    max_clicks = 5  # 5번 클릭 제한
    menu_button_active = False  # 메뉴 버튼 활성화 상태

    # 카테고리별 이미지 로드
    item_images = (
        [load_image(f'good{i}.png') for i in range(1, 4)] +
        [load_image(f'trash{i}.png') for i in range(1, 4)] +
        [load_image(f'rare{i}.png') for i in range(1, 4)] +
        [load_image(f'normal{i}.png') for i in range(1, 4)]
    )
    used_items = []  # 이미 선택된 아이템 저장 리스트


def finish():
    global background, button, current_image, item_images, used_items
    del background, button, current_image, item_images, used_items


def pick_item():
    """같은 아이템이 나오지 않게 무작위로 아이템 선택"""
    global used_items
    available_items = [item for item in item_images if item not in used_items]
    if available_items:
        chosen_item = random.choice(available_items)
        used_items.append(chosen_item)
        return chosen_item
    return None  # 선택 가능한 아이템이 없을 경우


def handle_events():
    global current_image, click_count, menu_button_active
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 900 - event.y
            # 시작 버튼 클릭
            if not menu_button_active and 800 - 50 <= x <= 800 + 50 and 100 - 25 <= y <= 100 + 25:
                if click_count < max_clicks:
                    current_image = pick_item()
                    if current_image:
                        click_count += 1
                    if click_count == max_clicks:  # 5번 클릭 완료 시
                        menu_button_active = True
            # 메뉴로 버튼 클릭
            elif menu_button_active and 750 <= x <= 850 and 175 <= y <= 225:  # "메뉴로" 버튼 범위
                a_game_framework.change_mode(a_menu)  # 메뉴로 전환



def draw():
    clear_canvas()
    background.draw(900, 450)
    if current_image:
        current_image.draw(900, 450)

    # 버튼 그리기 (시작 버튼은 크기 4배 줄임)
    button.clip_draw(0, 0, button.w, button.h, 800, 100, button.w // 4, button.h // 4)

    if menu_button_active:
        # "완료" 메시지 표시
        font = load_font('establish Retrosans.ttf', 40)
        font.draw(700, 500, "완료!", (255, 255, 0))
        # "메뉴로" 버튼 그리기
        draw_rectangle(750, 175, 850, 225)
        font.draw(760, 190, "메뉴로", (0, 0, 0))

    update_canvas()


def update():
    pass


def run(start_mode):

    global running
    running = True
    start_mode.init()  # 시작 모드 초기화
    while running:
        start_mode.handle_events()
        start_mode.update()
        start_mode.draw()
        delay(0.03)
    start_mode.finish()  # 종료 시 정리
