from pico2d import *

def init():
    global face_back, face, buttons, current_makeup
    face_back = load_image('face back.png')  # 배경 이미지
    face = load_image('face.png')  # 얼굴 이미지
    current_makeup = None

    # 버튼 설정
    colors = ['orange', 'purple', 'brown', 'blue', 'pink', 'green']
    buttons = [
        {'color': color, 'image': load_image(f'{color}.png'), 'makeup': load_image(f'makeup_{color}.png'),
         'x': 1700, 'y': 800 - i * 100} for i, color in enumerate(colors)
    ]

def finish():
    global face_back, face, buttons, current_makeup
    del face_back, face, buttons, current_makeup

def handle_events():
    global current_makeup
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 900 - event.y
            for button in buttons:
                if button['x'] - 50 <= x <= button['x'] + 50 and button['y'] - 50 <= y <= button['y'] + 50:
                    current_makeup = button['makeup']

def draw():
    clear_canvas()
    face_back.draw(900, 450)
    face.draw(900, 450)
    if current_makeup:
        current_makeup.draw(900, 450)

    for button in buttons:
        button['image'].draw(button['x'], button['y'])

    update_canvas()

def update():
    pass
