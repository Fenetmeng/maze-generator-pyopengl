# Maze Generator and Solver using PyOpenGL

## Description
This project is a computer graphics assignment implemented using Python, PyOpenGL, and Pygame. The program generates a random maze visually and then solves it using backtracking.

The maze generation uses a stack-based Depth-First Search (DFS) algorithm. A “mouse” starts from an initial cell and randomly moves to unvisited neighboring cells while removing walls between them. The previous cells are stored in a stack to support backtracking whenever the algorithm reaches a dead end. The process continues until all cells in the maze are visited.

After generating the maze, the program solves it using backtracking. The current valid path is shown in red, while dead-end paths are shown in blue.

## Features
- Dynamic maze generation
- Stack-based DFS traversal
- Backtracking maze solver
- PyOpenGL graphical visualization
- Animated wall removal and path solving

## Technologies Used
- Python
- PyOpenGL
- Pygame

## How to Run

Install dependencies:

pip install PyOpenGL PyOpenGL_accelerate pygame-ce

Run the project:

python maze.py

## Algorithms Used
- Depth-First Search (DFS)
- Stack-based Backtracking

## Visualization
- White lines = maze walls
- Red cells = current solution path
- Blue cells = dead ends
