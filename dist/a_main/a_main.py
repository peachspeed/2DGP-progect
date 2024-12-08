import a_game_framework
import a_logo_mode
from pico2d import*

# 캔버스 열기
open_canvas(1800, 900)

# 게임 실행
a_game_framework.run(a_logo_mode)

# 캔버스 닫기
close_canvas()
