"""
Main Entry Point for Pacman AI Game
Chạy file này để khởi động game
Nhóm 13: Pacman AI Development Team
"""

import sys
import os

# Thêm thư mục cha vào Python path để import được module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pygame

# Khởi tạo pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Import game từ module cuoi_ky_ttnt
try:
    from Nhom13_PacmanAI.game import Game
except ImportError:
    print("❌ Lỗi: Không thể import module cuoi_ky_ttnt!")
    print("Đảm bảo folder cuoi_ky_ttnt ở cùng cấp với Nhom13_PacmanAI")
    sys.exit(1)


def main():
    """Hàm main để chạy game"""
    print("🎮 Khởi động Pacman AI Game...")
    print("👥 Nhóm 13: Pacman AI Development Team")
    print("📋 Thành viên:")
    print("   - Nguyễn Minh Quốc Khánh (23110113)")
    print("   - Nguyễn Hưng Nguyên (23110135)")  
    print("   - Nguyễn Bách Tùng (23110166)")
    print("-" * 50)
    
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n🛑 Game stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("👋 Cảm ơn bạn đã chơi Pacman AI!")
        sys.exit()


if __name__ == "__main__":
    main()
