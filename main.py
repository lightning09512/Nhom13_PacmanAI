"""
Main Entry Point
Chạy file này để khởi động game
"""

import sys
import os

# Thêm thư mục cha vào Python path để import được module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

# Khởi tạo pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

from cuoi_ky_ttnt.game import Game


def main():
    """Hàm main để chạy game"""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
