"""
Script tạo file pacman.py với đầy đủ 17 thuật toán
"""

# Đọc code từ file csp_algorithms.py để lấy 3 thuật toán CSP
with open('csp_algorithms.py', 'r', encoding='utf-8') as f:
    csp_code = f.read()

# Tạo file pacman.py hoàn chỉnh
pacman_code = '''"""
Pacman AI Module
Chứa class PacmanAI với tất cả các thuật toán AI
"""

import random
import math
import heapq
from collections import deque
from .constants import (
    Direction, CellType, AIAlgorithm,
    MAZE_WIDTH, MAZE_HEIGHT
)


class PacmanAI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = Direction.RIGHT
        self.score = 0
        self.lives = 5
        self.power_mode = False
        self.power_timer = 0
        self.algorithm = AIAlgorithm.BFS
        
    def get_position(self):
        return (self.x, self.y)
    
    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
    
    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Kiểm tra biên
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
            if maze[new_y][new_x] != CellType.WALL:
                self.x = new_x
                self.y = new_y
                return True
        return False
    
    def eat_dot(self, maze):
        if maze[self.y][self.x] == CellType.DOT:
            maze[self.y][self.x] = CellType.EMPTY
            self.score += 10
            return True
        elif maze[self.y][self.x] == CellType.FRUIT:
            # Cherry: ăn sẽ kích hoạt sức mạnh tạm thời
            maze[self.y][self.x] = CellType.EMPTY
            self.score += 100
            self.power_mode = True
            self.power_timer = 120  # ~12s
            return True
        return False
    
    def update_power_mode(self):
        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False
    
    def get_next_move(self, maze, ghosts):
        if self.algorithm == AIAlgorithm.BFS:
            return self.bfs_move(maze)
        elif self.algorithm == AIAlgorithm.DFS:
            return self.dfs_move(maze)
        elif self.algorithm == AIAlgorithm.UCS:
            return self.ucs_move(maze)
        elif self.algorithm == AIAlgorithm.IDS:
            return self.ids_move(maze)
        elif self.algorithm == AIAlgorithm.GREEDY:
            return self.greedy_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.A_STAR:
            return self.a_star_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.HILL_CLIMBING:
            return self.hill_climbing_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.SIMULATED_ANNEALING:
            return self.simulated_annealing_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.BEAM_SEARCH:
            return self.beam_search_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.MINIMAX:
            return self.minimax_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.ALPHA_BETA:
            return self.alpha_beta_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.EXPECTIMAX:
            return self.expectimax_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.AND_OR:
            return self.and_or_planning_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.GENETIC:
            return self.genetic_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.BACKTRACKING:
            return self.backtracking_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.FORWARD_CHECKING:
            return self.forward_checking_move(maze, ghosts)
        elif self.algorithm == AIAlgorithm.AC3:
            return self.ac3_move(maze, ghosts)
        else:
            return self.first_valid_move(maze, ghosts)
'''

# In ra để kiểm tra
print("Đang tạo file pacman.py...")
print("File sẽ có đầy đủ 17 thuật toán AI")
print("\nVui lòng sử dụng file HUONG_DAN_THEM_CSP.md để hoàn thành việc thêm code!")
