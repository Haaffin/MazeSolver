from cell import Cell
import random
import time
import heapq


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        # time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def _solve_r(self, i, j):
        self._animate()

        self._cells[i][j].visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        return False

    def solve(self):
        open_set = []
        heapq.heappush(open_set, (0, 0, 0))  # (f, i, j)

        g_score = { (i, j): float('inf') for i in range(self._num_cols) for j in range(self._num_rows) }
        g_score[(0, 0)] = 0

        f_score = { (i, j): float('inf') for i in range(self._num_cols) for j in range(self._num_rows) }
        f_score[(0, 0)] = self._heuristic(0, 0)

        visited = set()

        while open_set:
            _, i, j = heapq.heappop(open_set)

            if i == self._num_cols - 1 and j == self._num_rows - 1:
                return True

            visited.add((i, j))
            self._cells[i][j].visited = True
            self._animate()

            neighbors = self._get_neighbors(i, j)
            for ni, nj in neighbors:
                if (ni, nj) in visited:
                    continue

                tentative_g_score = g_score[(i, j)] + 1 

                if tentative_g_score < g_score[(ni, nj)]:
                    g_score[(ni, nj)] = tentative_g_score
                    f_score[(ni, nj)] = tentative_g_score + self._heuristic(ni, nj)

                    heapq.heappush(open_set, (f_score[(ni, nj)], ni, nj))

                    self._cells[i][j].draw_move(self._cells[ni][nj])

        return False

    def _heuristic(self, i, j):
        """Heuristic function: Manhattan distance to the goal."""
        return abs(self._num_cols - 1 - i) + abs(self._num_rows - 1 - j)

    def _get_neighbors(self, i, j):
        """Get valid neighbors of a cell (i, j) considering walls."""
        neighbors = []
        if i > 0 and not self._cells[i][j].has_left_wall:  # Left
            neighbors.append((i - 1, j))
        if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall:  # Right
            neighbors.append((i + 1, j))
        if j > 0 and not self._cells[i][j].has_top_wall:  # Up
            neighbors.append((i, j - 1))
        if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall:  # Down
            neighbors.append((i, j + 1))
        return neighbors
