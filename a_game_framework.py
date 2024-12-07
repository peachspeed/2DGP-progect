stack = []
running = True

def change_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()

def run(start_mode):
    global running, stack
    stack.append(start_mode)
    start_mode.init()

    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

    while len(stack) > 0:
        stack[-1].finish()
        stack.pop()

def quit():
    global running
    running = False
