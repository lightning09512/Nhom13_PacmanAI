"""
Constants and Enums cho Pacman AI Game
Chứa tất cả các hằng số, màu sắc và enumerations
"""

from enum import Enum

# Window và Grid Constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 700  # Tăng từ 480 lên 700 để hiển thị đủ menu
GRID_SIZE = 20
MAZE_WIDTH = WINDOW_WIDTH // GRID_SIZE
MAZE_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Enhanced Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
YELLOW_DARK = (200, 200, 0)
RED = (255, 0, 0)
RED_DARK = (180, 0, 0)
BLUE = (0, 0, 255)
BLUE_DARK = (0, 0, 180)
PINK = (255, 192, 203)
PINK_DARK = (220, 150, 160)
ORANGE = (255, 165, 0)
ORANGE_DARK = (200, 120, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREEN_DARK = (0, 180, 0)
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# UI Colors
UI_BACKGROUND = (20, 20, 40)
UI_BORDER = (100, 100, 150)
UI_TEXT = (255, 255, 255)
UI_ACCENT = (255, 215, 0)  # Gold


class Direction(Enum):
    """Enum cho các hướng di chuyển"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class CellType(Enum):
    """Enum cho các loại ô trong maze"""
    EMPTY = 0
    WALL = 1
    DOT = 2
    POWER_PELLET = 3
    FRUIT = 4


class AIAlgorithm(Enum):
    """Enum cho các thuật toán AI"""
    BFS = "BFS"
    DFS = "DFS"
    UCS = "UCS"
    IDS = "IDS"
    IDL = "IDL"  # Iterative Deepening Limited
    GREEDY = "Greedy"
    A_STAR = "A*"
    HILL_CLIMBING = "Hill-Climbing"
    SIMULATED_ANNEALING = "Simulated Annealing"
    BEAM_SEARCH = "Beam Search"
    MINIMAX = "Minimax"
    ALPHA_BETA = "Alpha-Beta"
    EXPECTIMAX = "Expectimax"
    GENETIC = "Genetic"
    AND_OR = "And-Or Planning"
    BACKTRACKING = "Backtracking"  # CSP Algorithm
    FORWARD_CHECKING = "Forward Checking"  # CSP Algorithm
    AC3 = "AC-3"  # CSP Algorithm
