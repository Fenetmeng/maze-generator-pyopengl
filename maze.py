import pygame
from pygame.locals import *
from OpenGL.GL import *
import random

pygame.init()

screen_width = 800
screen_height = 600

rows = 10
cols = 15
cell_size = 40

start_x = 100
start_y = 80

pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Maze Generation & Solving")

glViewport(0, 0, screen_width, screen_height)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, screen_width, screen_height, 0, -1, 1)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.top = True
        self.right = True
        self.bottom = True
        self.left = True

        self.visited = False

        # solver states
        self.in_path = False
        self.dead_end = False

    def draw(self):
        x = start_x + self.col * cell_size
        y = start_y + self.row * cell_size

        # generated cells
        if self.visited:
            glColor3f(0.15, 0.15, 0.15)

            glBegin(GL_QUADS)
            glVertex2f(x + 1, y + 1)
            glVertex2f(x + cell_size - 1, y + 1)
            glVertex2f(x + cell_size - 1, y + cell_size - 1)
            glVertex2f(x + 1, y + cell_size - 1)
            glEnd()

        # red path
        if self.in_path:
            glColor3f(1, 0, 0)

            glBegin(GL_QUADS)
            glVertex2f(x + 8, y + 8)
            glVertex2f(x + cell_size - 8, y + 8)
            glVertex2f(x + cell_size - 8, y + cell_size - 8)
            glVertex2f(x + 8, y + cell_size - 8)
            glEnd()

        # blue dead ends
        if self.dead_end:
            glColor3f(0, 0, 1)

            glBegin(GL_QUADS)
            glVertex2f(x + 10, y + 10)
            glVertex2f(x + cell_size - 10, y + 10)
            glVertex2f(x + cell_size - 10, y + cell_size - 10)
            glVertex2f(x + 10, y + cell_size - 10)
            glEnd()

        glColor3f(1, 1, 1)
        glLineWidth(2)

        glBegin(GL_LINES)

        if self.top:
            glVertex2f(x, y)
            glVertex2f(x + cell_size, y)

        if self.right:
            glVertex2f(x + cell_size, y)
            glVertex2f(x + cell_size, y + cell_size)

        if self.bottom:
            glVertex2f(x, y + cell_size)
            glVertex2f(x + cell_size, y + cell_size)

        if self.left:
            glVertex2f(x, y)
            glVertex2f(x, y + cell_size)

        glEnd()


def get_unvisited_neighbors(cell):
    neighbors = []

    r = cell.row
    c = cell.col

    if r > 0 and not grid[r - 1][c].visited:
        neighbors.append(grid[r - 1][c])

    if c < cols - 1 and not grid[r][c + 1].visited:
        neighbors.append(grid[r][c + 1])

    if r < rows - 1 and not grid[r + 1][c].visited:
        neighbors.append(grid[r + 1][c])

    if c > 0 and not grid[r][c - 1].visited:
        neighbors.append(grid[r][c - 1])

    return neighbors


def remove_wall(current, next_cell):
    dr = current.row - next_cell.row
    dc = current.col - next_cell.col

    if dr == 1:
        current.top = False
        next_cell.bottom = False

    elif dr == -1:
        current.bottom = False
        next_cell.top = False

    elif dc == 1:
        current.left = False
        next_cell.right = False

    elif dc == -1:
        current.right = False
        next_cell.left = False


def get_possible_moves(cell):
    moves = []

    r = cell.row
    c = cell.col

    if not cell.top and r > 0:
        moves.append(grid[r - 1][c])

    if not cell.right and c < cols - 1:
        moves.append(grid[r][c + 1])

    if not cell.bottom and r < rows - 1:
        moves.append(grid[r + 1][c])

    if not cell.left and c > 0:
        moves.append(grid[r][c - 1])

    return moves


grid = []

for r in range(rows):
    row_cells = []

    for c in range(cols):
        row_cells.append(Cell(r, c))

    grid.append(row_cells)


# =========================
# MAZE GENERATION
# =========================

current_cell = grid[0][0]
current_cell.visited = True

stack = []

generation_finished = False

# =========================
# MAZE SOLVING
# =========================

solver_started = False
solver_finished = False

solver_stack = []

start_cell = grid[0][0]
end_cell = grid[rows - 1][cols - 1]

solve_current = start_cell

visited_solver = set()

clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # =========================
    # GENERATE MAZE
    # =========================

    if not generation_finished:

        neighbors = get_unvisited_neighbors(current_cell)

        if len(neighbors) > 0:

            next_cell = random.choice(neighbors)

            stack.append(current_cell)

            remove_wall(current_cell, next_cell)

            current_cell = next_cell
            current_cell.visited = True

        elif len(stack) > 0:

            current_cell = stack.pop()

        else:

            generation_finished = True

            # create entrance and exit
            start_cell.left = False
            end_cell.right = False

    # =========================
    # SOLVE MAZE
    # =========================

    elif not solver_finished:

        solver_started = True

        solve_current.in_path = True

        visited_solver.add((solve_current.row, solve_current.col))

        if solve_current == end_cell:

            solver_finished = True

        else:

            possible_moves = []

            for move in get_possible_moves(solve_current):

                pos = (move.row, move.col)

                if pos not in visited_solver:
                    possible_moves.append(move)

            if len(possible_moves) > 0:

                next_move = possible_moves[0]

                solver_stack.append(solve_current)

                solve_current = next_move

            elif len(solver_stack) > 0:

                solve_current.dead_end = True
                solve_current.in_path = False

                solve_current = solver_stack.pop()

    # =========================
    # DRAW
    # =========================

    glClear(GL_COLOR_BUFFER_BIT)

    for r in range(rows):
        for c in range(cols):
            grid[r][c].draw()

    pygame.display.flip()

    clock.tick(25)

pygame.quit()