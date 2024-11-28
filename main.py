import pico2d
import clothes

pico2d.open_canvas()

clothes.init()

while clothes.running:
    clothes.handle_events()
    clothes.update()
    clothes.draw()
    pico2d.delay(0.01)

clothes.finish()

pico2d.close_canvas()