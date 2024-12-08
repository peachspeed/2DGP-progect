stack = []

def run(start_mode):
    """
    start_mode: 처음 실행할 모드
    """
    global running
    stack.append(start_mode)
    start_mode.init()
    running = True
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
    while len(stack) > 0:
        stack[-1].finish()
        stack.pop()

def change_mode(new_mode):
    """
    현재 모드를 종료하고 새로운 모드를 실행
    """
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    stack.append(new_mode)
    new_mode.init()

def push_mode(new_mode):
    """
    현재 모드를 일시 정지하고 새로운 모드를 실행
    """
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(new_mode)
    new_mode.init()

def pop_mode():
    """
    현재 모드를 종료하고 이전 모드로 돌아감
    """
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    if len(stack) > 0:
        stack[-1].resume()
