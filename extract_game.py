"""
Script tự động tạo file game.py từ pacman_ai.py
"""

import re

# Đọc file gốc
with open('c:/Users/ztung/OneDrive/Desktop/MMT_23110166/pacman_ai.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Tìm class Game
game_class_match = re.search(r'class Game:.*', content, re.DOTALL)

if game_class_match:
    game_class_content = game_class_match.group(0)
    
    # Tạo header cho file game.py
    header = '''"""
Game Module
Chứa class Game với toàn bộ logic game chính
"""

import pygame
import sys
import random
import math
import json
import os
from .constants import *
from .sound_manager import SoundManager
from .pacman import PacmanAI
from .ghost import Ghost

'''
    
    # Ghi ra file
    with open('c:/Users/ztung/OneDrive/Desktop/MMT_23110166/cuoi_ky_ttnt/game.py', 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(game_class_content)
    
    print("✅ Đã tạo file game.py thành công!")
    print(f"   Độ dài: {len(game_class_content)} ký tự")
else:
    print("❌ Không tìm thấy class Game")
