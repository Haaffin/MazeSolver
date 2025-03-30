from graphics import Window
from maze import Maze
import sys
import time
import random

def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    sys.setrecursionlimit(10000)
    win = Window(screen_x, screen_y)

    while True:  
        seed = random.randint(1, 100000)  
        maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed)
        print(f"maze created with seed {seed}")

        start_time = time.time()
        is_solvable = maze.solve()
        end_time = time.time()

        elapsed_time = end_time - start_time

        if not is_solvable:
            print("maze can not be solved!")
            win.draw_text("Maze cannot be solved!", screen_x // 2, screen_y // 2, size=24, color="red")
        else:
            print(f"maze solved in {elapsed_time:.2f} seconds!")
            win.draw_text(f"Maze solved in {elapsed_time:.2f} seconds!", screen_x // 2, screen_y // 2, size=24, color="black")

        win.redraw()
        time.sleep(3)
        win.clear()

main()