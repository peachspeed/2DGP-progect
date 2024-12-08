from pico2d import load_image

class Ku:
    def __init__(self):
        self.x, self.y = 70, 150  # 500x500 화면 기준 오른쪽 밑
        self.frame = 0
        self.dir = 0
        self.action = 0
        self.act = 0  # 캐릭터의 동작 상태 (0 = 가만히, 1 = 걷기)
        self.walk_image = load_image('pixilart-sprite.png')
        self.stop_image = load_image('stop.png')
        self.a_state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def update(self):
        # 프레임을 계속 업데이트
        self.frame = (self.frame + 1) % 4
        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir = 1  # 오른쪽 이동 시작
                self.act = 1  # 걷기 동작

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.dir = 0  # 이동 멈춤
                self.act = 0  # 가만히 있는 동작

    def draw(self):
        self.state_machine.draw()


class Idle:
    @staticmethod
    def enter(ku):
        print('Boy Idle Enter')

    @staticmethod
    def exit(ku):
        print('Boy Idle Exit')

    @staticmethod
    def do(ku):
        ku.frame = (ku.frame + 1) % 8

    @staticmethod
    def draw(ku):
        if ku.act == 0:
            ku.stop_image.draw(ku.x, ku.y, 230, 230)
        else:
            ku.walk_image.clip_draw(ku.frame * 100, 100 * ku.action, 100, 100, ku.x, ku.y, 230, 230)