"""
Ghost Module
Chứa class Ghost cho AI của ghost
"""

import random
from constants import Direction, CellType, MAZE_WIDTH, MAZE_HEIGHT


class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice(list(Direction))
        self.speed = 1
        
    def get_position(self):
        return (self.x, self.y)
    
    def move(self, maze):
        """Di chuyển ghost ngẫu nhiên nhưng hợp lệ"""
        directions = list(Direction)
        random.shuffle(directions)
        
        for direction in directions:
            dx, dy = direction.value
            new_x = self.x + dx
            new_y = self.y + dy
            
            if (0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and
                maze[new_y][new_x] != CellType.WALL):
                self.x = new_x
                self.y = new_y
                self.direction = direction
                break
