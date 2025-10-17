"""
Main Entry Point for Pacman AI Game
Chạy file này để khởi động game
Nhóm 13: Pacman AI Development Team
"""

import sys
import os

# Đảm bảo làm việc tại thư mục chứa file này để các đường dẫn tài nguyên tương đối hoạt động trên mọi máy
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
# Bổ sung vào sys.path để Pylance/Python tìm được module cục bộ 'game', 'constants', ...
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import pygame

# Khởi tạo pygame (an toàn trên máy không có thiết bị âm thanh)
pygame.init()
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
except Exception as audio_err:
    # Cho phép chạy không âm thanh nếu hệ thống không có thiết bị audio
    print(f"⚠️ Không thể khởi tạo âm thanh: {audio_err}. Tiếp tục chạy không âm thanh.")

# Import Game với 2 chế độ: chạy như script (from game) hoặc như package (Nhom13_PacmanAI.game) bằng importlib
try:
    from game import Game  # khi chạy: python main.py
except ImportError:
    try:
        import importlib
        Game = importlib.import_module("Nhom13_PacmanAI.game").Game  # khi chạy: python -m Nhom13_PacmanAI.main
    except Exception as imp_err:
        print("❌ Lỗi: Không thể import module 'game'. Hãy đảm bảo bạn đang chạy từ thư mục dự án chứa file game.py")
        print("Gợi ý chạy 1: python main.py")
        print("Gợi ý chạy 2: python -m Nhom13_PacmanAI.main")
        print(f"Chi tiết: {imp_err}")
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
