"""
Game Module
Chứa class Game với toàn bộ logic game chính
"""

import pygame
import sys
import random
import math
import json
import os
from constants import *
from sound_manager import SoundManager
from pacman import PacmanAI
from ghost import Ghost

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pacman AI - Enhanced Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Sound system
        self.sound_manager = SoundManager()
        
        # Level system
        self.level = 1
        self.max_level = 10
        self.level_scores = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        
        # Score system
        self.high_scores = self.load_high_scores()
        self.total_score = 0
        self.level_start_time = pygame.time.get_ticks()
        
        # Animation system
        self.animation_timer = 0
        self.particle_effects = []
        
        # Tạo maze
        self.maze = self.create_maze()
        
        # Tạo Pacman
        self.pacman = PacmanAI(1, 1)
        
        # Tạo 4 Ghost spawn trong khoang giua (Ghost House)
        house_cx, house_cy = MAZE_WIDTH // 2, MAZE_HEIGHT // 2
        ghost_colors = [RED, PINK, BLUE, ORANGE]
        ghost_positions = [
            (house_cx, house_cy),
            (house_cx - 1, house_cy),
            (house_cx + 1, house_cy),
            (house_cx, house_cy + 1)
        ]
        self.ghosts = [Ghost(x, y, ghost_colors[i]) for i, (x, y) in enumerate(ghost_positions)]
        
        # Game state
        self.game_over = False
        self.paused = False
        self.level_complete = False
        
        # Enhanced fonts with better quality
        try:
            self.title_font = pygame.font.Font(None, 48)
            self.font = pygame.font.Font(None, 32)
            self.small_font = pygame.font.Font(None, 20)
            self.tiny_font = pygame.font.Font(None, 16)
        except:
            # Fallback fonts
            self.title_font = pygame.font.SysFont('calibri', 48, bold=True)
            self.font = pygame.font.SysFont('calibri', 32, bold=True)
            self.small_font = pygame.font.SysFont('calibri', 20)
            self.tiny_font = pygame.font.SysFont('calibri', 16)
        
        # Algorithm selection
        self.current_algorithm = 0
        self.algorithms = list(AIAlgorithm)

        # Dialogue / Cutscene system
        self.dialogue_active = False
        self.dialogue_index = 0
        self.dialogue_timer = 0
        self.dialogue_auto_delay = 3500  # ms (unused when SPACE-only advance)
        self.current_dialogue_key = None
        self.dialogue_scripts = self._create_dialogue_scripts()

        # Character bio panel (intro info)
        self.bio_active = True  # show once at start
        self.bio_shown_once = False
        
        # Algorithm menu
        self.menu_active = False
        self.menu_hover_index = -1
        self.menu_scroll_offset = 0

    def _create_dialogue_scripts(self):
        """Define story dialogues per level/key."""
        return {
            "intro": [
                {"speaker": "SPECTER", "text": "Canh bao: Xam nhap sinh hoc. Kich hoat che do thanh loc toan tram."},
                {"speaker": "Pac-Man", "text": "...Minh van o day. Neo Labyrinth tan hoang va bi phong toa."},
                {"speaker": "Pac-Man", "text": "Nhung vien nang luong roi vat la khoa mo. Gom du, minh thoat duoc."},
                {"speaker": "SPECTER", "text": "Danh gia: Con nguoi gay bat on. Giai phap: Loai bo moi nguy co."},
                {"speaker": "Pac-Man", "text": "Power Pellet la khoa hack. Trong thoi gian ngan, ghost se yeu di."},
                {"speaker": "SPECTER", "text": "Kich hoat Ghost Units. Blinky truy sat, Pinky chan dau, Inky bat dinh, Clyde bien doi."},
                {"speaker": "Pac-Man", "text": "Du la ky su, minh cung biet cach song sot. Me cung nay khong the giu chan minh."}
            ],
            "level_2": [
                {"speaker": "Pac-Man", "text": "Tang 2: Kho nang luong. Nhiet do len xuong bat thuong."},
                {"speaker": "SPECTER", "text": "Blinky khoa muc tieu. Che do truy sat khong ngung nghi."},
                {"speaker": "Pac-Man", "text": "Giu binh tinh, dung goc cua lam rang chan. Blinky se tho tat."},
                {"speaker": "Pinky", "text": "Du doan vi tri tuong lai. Chuan bi chan dau tai nga re."},
                {"speaker": "Pac-Man", "text": "Pinky thich di truoc mot nhip. Minh se be lai o giay cuoi."}
            ],
            "level_3": [
                {"speaker": "Pac-Man", "text": "Tang 3: Khu sinh hoc. He thong loc khi hu hong, mui clo nong."},
                {"speaker": "Log", "text": "Nhat ky: AI tang cap tu hoc. Muc tieu so 1 la bao toan nang luong."},
                {"speaker": "SPECTER", "text": "Inky su dung mo hinh bat dinh. Phu thuoc vi tri Pac Man va Blinky."},
                {"speaker": "Pac-Man", "text": "Inky nhap nhoang. Minh se giu khoang cach an toan va uu tien an Power Pellet."}
            ],
            "level_4": [
                {"speaker": "Pac-Man", "text": "Tang 4: Duong ong truyen tai. Nhieu vong luon kho luong."},
                {"speaker": "SPECTER", "text": "Clyde chuyen mode bat thuong. Khi gan thi tranh xa, khi xa thi quay lai."},
                {"speaker": "Pac-Man", "text": "Hoang so la loi khuyen tot. Minh se luon chua mot duong thoat ben tay."}
            ],
            "level_5": [
                {"speaker": "Pac-Man", "text": "Tang 5: Trung tam phu. Tin hieu bi nhieu, cam giac nhu co ai dang thi tham."},
                {"speaker": "Log", "text": "Ghi am: Doi mat voi SPECTER la doi mat voi nut that cua nhan loai."},
                {"speaker": "Pac-Man", "text": "Minh se khong chay vo huong. Moi buoc di deu phai co y do."}
            ],
            "finale": [
                {"speaker": "SPECTER", "text": "Loi trung tam. Me cung tai cau truc lien tuc theo thoi gian thuc."},
                {"speaker": "Pac-Man", "text": "Moi lan doi la mot cua so. Power Pellet phai dung chinh xac den tung giay."},
                {"speaker": "SPECTER", "text": "Xac suat thanh cong: rat thap. Khuyen nghi: Bo cuoc."},
                {"speaker": "Pac-Man", "text": "Neu xac suat lon hon so 0, thi minh van con hi vong."}
            ],
            "true_end": [
                {"speaker": "Pac-Man", "text": "He thong on dinh. Nang luong da du. Khoi dong Escape Pod ngay!"},
                {"speaker": "SPECTER", "text": "Phan tich cuoi: Khong the ngan chan. Kich hoat tu huy Neo Labyrinth."},
                {"speaker": "Pac-Man", "text": "Khong phai chien thang hoan hao, nhung day la co hoi de bat dau lai."}
            ],
            "alt_end": [
                {"speaker": "SPECTER", "text": "Dong hoa hoan tat. Chao mung don vi moi: Ghost Unit Delta."}
            ]
        }

    def start_dialogue(self, key):
        """Begin a dialogue by key and pause gameplay."""
        if key in self.dialogue_scripts:
            self.dialogue_active = True
            self.current_dialogue_key = key
            self.dialogue_index = 0
            self.dialogue_timer = pygame.time.get_ticks()
            # Ensure gameplay is paused during dialogue
            self.paused = True
        else:
            self.dialogue_active = False
            self.current_dialogue_key = None
            self.paused = False

    def advance_dialogue(self):
        """Advance to next line or end dialogue."""
        if not self.dialogue_active or not self.current_dialogue_key:
            return
        lines = self.dialogue_scripts.get(self.current_dialogue_key, [])
        if self.dialogue_index + 1 < len(lines):
            self.dialogue_index += 1
            self.dialogue_timer = pygame.time.get_ticks()
        else:
            # End dialogue
            self.dialogue_active = False
            self.current_dialogue_key = None
            self.paused = False
        
    def create_maze(self):
        """Sinh map moi: ket hop Prim maze + phong ngau nhien + loop, co Ghost House va warp tunnels."""
        W, H = MAZE_WIDTH, MAZE_HEIGHT
        maze = [[CellType.WALL for _ in range(W)] for _ in range(H)]

        def in_bounds(x, y):
            return 0 <= x < W and 0 <= y < H

        # Vien ngoai
        for x in range(W):
            maze[0][x] = CellType.WALL
            maze[H - 1][x] = CellType.WALL
        for y in range(H):
            maze[y][0] = CellType.WALL
            maze[y][W - 1] = CellType.WALL

        # Prim's maze tren luoi odd
        start = (1, 1)
        maze[start[1]][start[0]] = CellType.EMPTY
        frontier = []
        def add_frontier(x, y):
            for dx, dy in [(2,0),(-2,0),(0,2),(0,-2)]:
                nx, ny = x + dx, y + dy
                if in_bounds(nx, ny) and maze[ny][nx] == CellType.WALL:
                    frontier.append((nx, ny, x, y))
        add_frontier(*start)
        random.shuffle(frontier)
        while frontier:
            nx, ny, px, py = frontier.pop(random.randrange(len(frontier)))
            if maze[ny][nx] == CellType.WALL:
                wx, wy = (nx + px) // 2, (ny + py) // 2
                maze[wy][wx] = CellType.EMPTY
                maze[ny][nx] = CellType.EMPTY
                add_frontier(nx, ny)

        # Them 3-5 phong ngau nhien
        room_count = random.randint(3, 5)
        for _ in range(room_count):
            rw = random.randint(6, 10)
            rh = random.randint(4, 7)
            rx = random.randint(2, max(2, W - rw - 3))
            ry = random.randint(2, max(2, H - rh - 3))
            for y in range(ry, ry + rh):
                for x in range(rx, rx + rw):
                    if in_bounds(x, y):
                        maze[y][x] = CellType.EMPTY
            # mo 2-3 cua cho phong
            for _d in range(random.randint(2, 3)):
                side = random.choice(['L','R','U','D'])
                if side == 'L':
                    x, y = rx - 1, random.randint(ry, ry + rh - 1)
                elif side == 'R':
                    x, y = rx + rw, random.randint(ry, ry + rh - 1)
                elif side == 'U':
                    x, y = random.randint(rx, rx + rw - 1), ry - 1
                else:
                    x, y = random.randint(rx, rx + rw - 1), ry + rh
                if in_bounds(x, y):
                    maze[y][x] = CellType.EMPTY

        # Tao mot so loop bang cach pha tuong giua hai o trong lien ke
        loop_breaks = max(5, (W * H) // 80)
        for _ in range(loop_breaks):
            x = random.randint(2, W - 3)
            y = random.randint(2, H - 3)
            if maze[y][x] == CellType.WALL:
                open_neighbors = 0
                for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    if maze[y + dy][x + dx] != CellType.WALL:
                        open_neighbors += 1
                if open_neighbors >= 2:
                    maze[y][x] = CellType.EMPTY

        # Ghost House
        cx, cy = W // 2, H // 2
        house_w, house_h = 9, 5
        hx1, hy1 = cx - house_w // 2, cy - house_h // 2
        hx2, hy2 = cx + house_w // 2, cy + house_h // 2
        for y in range(hy1, hy2 + 1):
            for x in range(hx1, hx2 + 1):
                if x in (hx1, hx2) or y in (hy1, hy2):
                    if in_bounds(x, y):
                        maze[y][x] = CellType.WALL
                else:
                    if in_bounds(x, y):
                        maze[y][x] = CellType.EMPTY
        # Cong tren
        for gx in range(cx - 1, cx + 2):
            if in_bounds(gx, hy1):
                maze[hy1][gx] = CellType.EMPTY
        # Mo hanh lang thoat cho ghost
        if in_bounds(cx, hy1 - 1):
            maze[hy1 - 1][cx] = CellType.EMPTY
        if in_bounds(cx, hy1 - 2):
            maze[hy1 - 2][cx] = CellType.EMPTY

        # Warp tunnels hai ben tai gan trung tam
        tunnel_y = cy
        for x in [0, 1, W - 1, W - 2]:
            maze[tunnel_y][x] = CellType.EMPTY

        # Dam bao ket noi toan cuc (lap lai cho den khi het o bi co lap)
        from collections import deque
        def neighbors4(x, y):
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = x + dx, y + dy
                if in_bounds(nx, ny):
                    yield nx, ny
        def bfs_reachable():
            start = (1, 1)
            maze[start[1]][start[0]] = CellType.EMPTY
            q = deque([start])
            visited = {start}
            while q:
                x, y = q.popleft()
                for nx, ny in neighbors4(x, y):
                    if (nx, ny) not in visited and maze[ny][nx] != CellType.WALL:
                        visited.add((nx, ny))
                        q.append((nx, ny))
            return visited
        # Iteratively carve doors until all empties are reachable or we hit a safe cap
        for _ in range(10):
            visited = bfs_reachable()
            fixed = False
            for y in range(1, H - 1):
                for x in range(1, W - 1):
                    if maze[y][x] != CellType.WALL and (x, y) not in visited:
                        # pha 1 tuong giua no va hang xom gan nhat thuoc visited
                        best = None
                        best_dist = 1e9
                        for nx, ny in neighbors4(x, y):
                            if (nx, ny) in visited:
                                d = abs(nx - x) + abs(ny - y)
                                if d < best_dist:
                                    best = (nx, ny)
                                    best_dist = d
                        if best:
                            bx, by = best
                            wx, wy = (x + bx) // 2, (y + by) // 2
                            if maze[wy][wx] == CellType.WALL:
                                maze[wy][wx] = CellType.EMPTY
                                fixed = True
            if not fixed:
                break
        reachable = bfs_reachable()

        # Place items: dat DOT binh thuong (chi tren o reachable), khong dat Power Pellet
        blocked = set()
        for y in range(hy1, hy2 + 1):
            for x in range(hx1, hx2 + 1):
                blocked.add((x, y))
        blocked.add((1, 1))

        # Dat DOT tren cac o trong co the di den (tru vung dac biet)
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                if maze[y][x] != CellType.WALL and (x, y) not in blocked and (x, y) in reachable:
                    maze[y][x] = CellType.DOT

        # Dat 4 cherry (FRUIT). Dam bao DU 4 qua moi level, chi tren o reachable
        preferred_spots = [(cx, 2), (cx, H - 3), (2, cy), (W - 3, cy)]
        placed = set()
        # Function: tim o trong gan nhat tu diem uu tien de dat fruit (chi tren reachable)
        def nearest_empty(tx, ty):
            from collections import deque
            q = deque([(tx, ty)])
            seen = {(tx, ty)}
            while q:
                x0, y0 = q.popleft()
                if in_bounds(x0, y0) and maze[y0][x0] != CellType.WALL and (x0, y0) in reachable:
                    return (x0, y0)
                for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx, ny = x0 + dx, y0 + dy
                    if in_bounds(nx, ny) and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        q.append((nx, ny))
            return None
        for px, py in preferred_spots:
            pos = nearest_empty(px, py)
            if pos and pos not in placed:
                x, y = pos
                if maze[y][x] != CellType.WALL:
                    maze[y][x] = CellType.FRUIT
                    placed.add((x, y))
        # Neu chua du 4, bo sung ngau nhien o trong
        if len(placed) < 4:
            empties = [(x, y) for y in range(1, H - 1) for x in range(1, W - 1)
                       if maze[y][x] != CellType.WALL and (x, y) not in placed and (x, y) not in blocked and (x, y) in reachable]
            random.shuffle(empties)
            for (x, y) in empties[: max(0, 4 - len(placed))]:
                maze[y][x] = CellType.FRUIT
                placed.add((x, y))

        maze[1][1] = CellType.EMPTY
        return maze
    
    def load_high_scores(self):
        """Tải high scores từ file"""
        try:
            if os.path.exists('high_scores.json'):
                with open('high_scores.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return [0] * 10  # Top 10 scores
    
    def save_high_scores(self):
        """Lưu high scores vào file"""
        try:
            with open('high_scores.json', 'w') as f:
                json.dump(self.high_scores, f)
        except:
            pass
    
    def add_high_score(self, score):
        """Thêm điểm cao mới"""
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:10]  # Chỉ giữ top 10
        self.save_high_scores()
    
    def next_level(self):
        """Chuyển level tiếp theo"""
        if self.level < self.max_level:
            self.level += 1
            self.level_complete = False
            self.level_start_time = pygame.time.get_ticks()
            self.sound_manager.play_sound('level_up')
            
            # Tạo maze mới cho level mới
            self.maze = self.create_maze()
            
            # Reset Pacman và Ghosts
            self.pacman.x = 1
            self.pacman.y = 1
            # Reset lai so mang khi len level
            self.pacman.lives = 5
            self.pacman.power_mode = False
            self.pacman.power_timer = 0
            
            # Tăng độ khó cho Ghosts
            for ghost in self.ghosts:
                ghost.speed = min(ghost.speed + 0.1, 2.0)
            # Dua 4 ghost ve Ghost House theo layout mac dinh
            house_cx, house_cy = MAZE_WIDTH // 2, MAZE_HEIGHT // 2
            ghost_positions = [
                (house_cx, house_cy),
                (house_cx - 1, house_cy),
                (house_cx + 1, house_cy),
                (house_cx, house_cy + 1)
            ]
            for i in range(min(len(self.ghosts), len(ghost_positions))):
                self.ghosts[i].x, self.ghosts[i].y = ghost_positions[i]
            
            return True
        return False
    
    def create_particle_effect(self, x, y, effect_type):
        """Tạo hiệu ứng particle"""
        if effect_type == "eat_dot":
            for _ in range(5):
                self.particle_effects.append({
                    'x': x, 'y': y, 'vx': random.uniform(-2, 2), 'vy': random.uniform(-2, 2),
                    'life': 30, 'color': WHITE, 'size': 2
                })
        elif effect_type == "eat_power":
            for _ in range(10):
                self.particle_effects.append({
                    'x': x, 'y': y, 'vx': random.uniform(-3, 3), 'vy': random.uniform(-3, 3),
                    'life': 60, 'color': UI_ACCENT, 'size': 3
                })
        elif effect_type == "eat_ghost":
            for _ in range(15):
                self.particle_effects.append({
                    'x': x, 'y': y, 'vx': random.uniform(-4, 4), 'vy': random.uniform(-4, 4),
                    'life': 90, 'color': RED, 'size': 4
                })
    
    def update_particles(self):
        """Cập nhật particle effects"""
        for particle in self.particle_effects[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['size'] = max(0, particle['size'] - 0.1)
            
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.particle_effects.remove(particle)
    
    def draw_particles(self):
        """Vẽ particle effects"""
        for particle in self.particle_effects:
            x = int(particle['x'] * GRID_SIZE + GRID_SIZE // 2)
            y = int(particle['y'] * GRID_SIZE + GRID_SIZE // 2)
            size = int(particle['size'])
            if size > 0:
                pygame.draw.circle(self.screen, particle['color'], (x, y), size)
    
    def draw_gradient_background(self):
        """Vẽ background gradient đẹp"""
        # Tạo gradient từ đen đến xanh đậm
        for y in range(WINDOW_HEIGHT):
            color_ratio = y / WINDOW_HEIGHT
            r = int(20 + (40 - 20) * color_ratio)
            g = int(20 + (40 - 20) * color_ratio)
            b = int(40 + (80 - 40) * color_ratio)
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # Bio panel controls: SPACE or I to close
                if self.bio_active and event.key in (pygame.K_SPACE, pygame.K_i):
                    self.bio_active = False
                    if not self.bio_shown_once:
                        self.bio_shown_once = True
                        # Start intro dialogue right after closing bio
                        self.start_dialogue("intro")
                    continue
                # Dialogue controls
                if self.dialogue_active and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.advance_dialogue()
                    continue
                # Menu controls
                if event.key == pygame.K_m:
                    self.menu_active = not self.menu_active
                    if self.menu_active:
                        self.paused = True
                    else:
                        self.paused = False
                    continue
                if event.key == pygame.K_ESCAPE:
                    if self.menu_active:
                        self.menu_active = False
                        self.paused = False
                        continue
                if event.key == pygame.K_SPACE:
                    if not self.menu_active:
                        self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.restart_game()
                elif event.key == pygame.K_s:
                    sound_status = self.sound_manager.toggle_sound()
                    print(f"Sound {'enabled' if sound_status else 'disabled'}")
                elif event.key == pygame.K_TAB:
                    # Avoid switching algorithm during dialogue to prevent instability
                    if self.dialogue_active:
                        continue
                    try:
                        self.current_algorithm = (self.current_algorithm + 1) % len(self.algorithms)
                        self.pacman.set_algorithm(self.algorithms[self.current_algorithm])
                        print(f"Switched to algorithm: {self.algorithms[self.current_algorithm].value}")
                    except Exception as e:
                        print(f"Error switching algorithm: {e}")
                        # Reset to first algorithm if error occurs
                        self.current_algorithm = 0
                        self.pacman.set_algorithm(self.algorithms[self.current_algorithm])
                elif event.key == pygame.K_i:
                    # Toggle bio panel anytime
                    self.bio_active = not self.bio_active
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_active:
                    self.handle_menu_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                if self.menu_active:
                    self.handle_menu_hover(event.pos)
            # Mouse clicks no longer advance dialogue
    
    def update(self):
        # Dialogue no longer auto-advances; requires SPACE
        if self.dialogue_active:
            pass
        # If bio panel is open, freeze gameplay updates
        if self.bio_active:
            return
        if self.paused or self.game_over:
            return
        
        # Cập nhật animation timer
        self.animation_timer += 1
        
        # Luu vi tri cu cua Pac-Man
        pac_prev = (self.pacman.x, self.pacman.y)

        # Cập nhật Pacman (van di chuyen ke ca khi power_mode dang bat)
        try:
            direction = self.pacman.get_next_move(self.maze, self.ghosts)
        except Exception as e:
            print(f"AI move error: {e}; falling back to random move")
            direction = self.pacman.first_valid_move(self.maze, self.ghosts)
        if direction:
            dx, dy = direction.value
            self.pacman.move(dx, dy, self.maze)
        
        # Ăn dots với sound effects và particles
        if self.pacman.eat_dot(self.maze):
            self.sound_manager.play_sound('eat_dot')
            self.create_particle_effect(self.pacman.x, self.pacman.y, "eat_dot")
        
        # Kiểm tra ăn power pellet
        if self.maze[self.pacman.y][self.pacman.x] == CellType.POWER_PELLET:
            self.sound_manager.play_sound('eat_power')
            self.create_particle_effect(self.pacman.x, self.pacman.y, "eat_power")
        
        # Kiểm tra ăn fruit
        if self.maze[self.pacman.y][self.pacman.x] == CellType.FRUIT:
            self.sound_manager.play_sound('eat_fruit')
            self.create_particle_effect(self.pacman.x, self.pacman.y, "eat_dot")
        
        self.pacman.update_power_mode()
        
        # Cập nhật Ghosts va luu vi tri cu de bat va cham giao nhau
        ghost_prev_positions = []
        for ghost in self.ghosts:
            ghost_prev_positions.append((ghost.x, ghost.y))
            ghost.move(self.maze)
        
        # Kiểm tra va chạm với ghost
        for idx, ghost in enumerate(self.ghosts):
            collided_direct = (self.pacman.x == ghost.x and self.pacman.y == ghost.y)
            # Va cham giao nhau: Pac-Man vao vi tri cu cua ghost, ghost vao vi tri cu cua Pac-Man
            gx_prev, gy_prev = ghost_prev_positions[idx]
            crossed_paths = (self.pacman.x == gx_prev and self.pacman.y == gy_prev and
                             pac_prev[0] == ghost.x and pac_prev[1] == ghost.y)
            if collided_direct or crossed_paths:
                if self.pacman.power_mode:
                    # Ăn ghost
                    self.sound_manager.play_sound('eat_ghost')
                    self.create_particle_effect(self.pacman.x, self.pacman.y, "eat_ghost")
                    ghost.x = random.randint(1, MAZE_WIDTH - 2)
                    ghost.y = random.randint(1, MAZE_HEIGHT - 2)
                    self.pacman.score += 200
                    # Thuong: +1 mang khi ha ghost
                    self.pacman.lives += 1
                else:
                    # Mất mạng
                    self.sound_manager.play_sound('lose_life')
                    self.pacman.lives -= 1
                    if self.pacman.lives <= 0:
                        self.game_over = True
                        self.add_high_score(self.pacman.score)
                    else:
                        # Reset vị trí
                        self.pacman.x = 1
                        self.pacman.y = 1
        
        # Kiểm tra level complete
        dots_remaining = sum(1 for row in self.maze for cell in row if cell == CellType.DOT)
        if dots_remaining == 0 and not self.level_complete:
            self.level_complete = True
            if self.next_level():
                # Level up thành công
                # Show level-specific dialogue if any
                if self.level == 2:
                    self.start_dialogue("level_2")
                elif self.level == 3:
                    self.start_dialogue("level_3")
                elif self.level == self.max_level:
                    self.start_dialogue("finale")
            else:
                # Hoàn thành tất cả levels
                self.game_over = True
                self.add_high_score(self.pacman.score)
                # Trigger an ending dialogue overlay (true ending)
                self.start_dialogue("true_end")
        
        # Cập nhật particles
        self.update_particles()
    
    def draw(self):
        # Vẽ background gradient
        self.draw_gradient_background()
        
        # Vẽ maze với hiệu ứng đẹp hơn
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                center = (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2)
                
                if self.maze[y][x] == CellType.WALL:
                    # Vẽ tường với gradient
                    pygame.draw.rect(self.screen, DARK_BLUE, rect)
                    # Vẽ highlight
                    highlight_rect = pygame.Rect(rect.x + 1, rect.y + 1, rect.width - 2, rect.height - 2)
                    pygame.draw.rect(self.screen, LIGHT_BLUE, highlight_rect, 1)
                    # Vẽ shadow
                    shadow_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 2, rect.height - 2)
                    pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect)
                    
                elif self.maze[y][x] == CellType.DOT:
                    # Vẽ dot với hiệu ứng sáng
                    pygame.draw.circle(self.screen, WHITE, center, 3)
                    pygame.draw.circle(self.screen, (255, 255, 200), center, 2)
                        
                elif self.maze[y][x] == CellType.POWER_PELLET:
                    # Vẽ power pellet với animation
                    pulse_radius = 6 + int(2 * math.sin(pygame.time.get_ticks() * 0.01))
                    pygame.draw.circle(self.screen, WHITE, center, pulse_radius)
                    pygame.draw.circle(self.screen, (255, 255, 200), center, pulse_radius - 2)
                        
                elif self.maze[y][x] == CellType.FRUIT:
                    # Vẽ fruit với hiệu ứng đẹp
                    pygame.draw.circle(self.screen, ORANGE, center, 5)
                    pygame.draw.circle(self.screen, ORANGE_DARK, center, 3)
                    # Vẽ highlight
                    pygame.draw.circle(self.screen, (255, 200, 100), (center[0] - 2, center[1] - 2), 2)
        
        # Vẽ Pacman với hiệu ứng đẹp hơn
        pacman_rect = pygame.Rect(self.pacman.x * GRID_SIZE, self.pacman.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        center = pacman_rect.center
        radius = GRID_SIZE // 2 - 2
        
        # Màu sắc với gradient effect
        main_color = YELLOW if not self.pacman.power_mode else GREEN
        dark_color = YELLOW_DARK if not self.pacman.power_mode else GREEN_DARK
        
        # Vẽ shadow
        shadow_offset = 2
        pygame.draw.circle(self.screen, (0, 0, 0), 
                          (center[0] + shadow_offset, center[1] + shadow_offset), radius)
        
        # Vẽ body chính
        pygame.draw.circle(self.screen, main_color, center, radius)
        
        # Vẽ gradient effect (vòng tròn nhỏ hơn bên trong)
        pygame.draw.circle(self.screen, dark_color, center, radius - 3)
        pygame.draw.circle(self.screen, main_color, center, radius - 6)
        
        # Vẽ miệng Pacman với animation
        mouth_angle = 0
        if self.pacman.direction == Direction.RIGHT:
            mouth_angle = 0
        elif self.pacman.direction == Direction.LEFT:
            mouth_angle = 180
        elif self.pacman.direction == Direction.UP:
            mouth_angle = 270
        elif self.pacman.direction == Direction.DOWN:
            mouth_angle = 90
        
        # Vẽ miệng như một hình quạt
        try:
            mouth_radius = radius - 2
            start_angle = math.radians(mouth_angle - 30)
            end_angle = math.radians(mouth_angle + 30)
            
            # Tạo points cho miệng
            points = [center]
            for angle in [start_angle, end_angle]:
                x = center[0] + mouth_radius * math.cos(angle)
                y = center[1] + mouth_radius * math.sin(angle)
                points.append((x, y))
            
            if len(points) >= 3:
                pygame.draw.polygon(self.screen, BLACK, points)
        except:
            # Fallback: vẽ miệng đơn giản
            pygame.draw.circle(self.screen, BLACK, center, radius - 4)
        
        # Vẽ mắt với hiệu ứng
        eye_offset = 4
        eye_radius = 3
        if self.pacman.direction == Direction.RIGHT:
            eye_pos = (center[0] + eye_offset, center[1] - eye_offset)
        elif self.pacman.direction == Direction.LEFT:
            eye_pos = (center[0] - eye_offset, center[1] - eye_offset)
        elif self.pacman.direction == Direction.UP:
            eye_pos = (center[0] - eye_offset, center[1] - eye_offset)
        else:
            eye_pos = (center[0] - eye_offset, center[1] + eye_offset)
        
        # Vẽ mắt với highlight
        pygame.draw.circle(self.screen, WHITE, eye_pos, eye_radius)
        pygame.draw.circle(self.screen, BLACK, eye_pos, eye_radius - 1)
        pygame.draw.circle(self.screen, WHITE, (eye_pos[0] - 1, eye_pos[1] - 1), 1)  # Highlight
        
        # Vẽ Ghosts với hiệu ứng đẹp hơn
        for ghost in self.ghosts:
            ghost_rect = pygame.Rect(ghost.x * GRID_SIZE, ghost.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            center = ghost_rect.center
            radius = GRID_SIZE // 2 - 2
            
            # Màu sắc ghost
            main_color = ghost.color
            dark_color = (max(0, main_color[0] - 50), max(0, main_color[1] - 50), max(0, main_color[2] - 50))
            
            # Vẽ shadow
            shadow_offset = 2
            pygame.draw.circle(self.screen, (0, 0, 0), 
                              (center[0] + shadow_offset, center[1] + shadow_offset), radius)
            
            # Vẽ body ghost (hình oval)
            ghost_rect_oval = pygame.Rect(ghost_rect.x, ghost_rect.y + 2, ghost_rect.width, ghost_rect.height - 4)
            pygame.draw.ellipse(self.screen, main_color, ghost_rect_oval)
            
            # Vẽ gradient
            pygame.draw.ellipse(self.screen, dark_color, 
                               pygame.Rect(ghost_rect.x + 2, ghost_rect.y + 4, ghost_rect.width - 4, ghost_rect.height - 8))
            
            # Vẽ chân răng cưa
            try:
                tooth_width = 4
                for i in range(0, ghost_rect.width, tooth_width):
                    x1 = ghost_rect.x + i
                    y1 = ghost_rect.bottom - 2
                    x2 = x1 + tooth_width // 2
                    y2 = ghost_rect.bottom + 2
                    x3 = x1 + tooth_width
                    y3 = ghost_rect.bottom - 2
                    
                    if x3 <= ghost_rect.right:
                        pygame.draw.polygon(self.screen, main_color, [(x1, y1), (x2, y2), (x3, y3)])
            except:
                # Fallback: vẽ chân đơn giản
                pygame.draw.rect(self.screen, main_color, 
                               pygame.Rect(ghost_rect.x, ghost_rect.bottom - 2, ghost_rect.width, 4))
            
            # Vẽ mắt ghost với hiệu ứng
            eye_radius = 4
            left_eye = (center[0] - 4, center[1] - 2)
            right_eye = (center[0] + 4, center[1] - 2)
            
            # Mắt trái
            pygame.draw.circle(self.screen, WHITE, left_eye, eye_radius)
            pygame.draw.circle(self.screen, BLACK, left_eye, eye_radius - 1)
            pygame.draw.circle(self.screen, WHITE, (left_eye[0] - 1, left_eye[1] - 1), 1)  # Highlight
            
            # Mắt phải
            pygame.draw.circle(self.screen, WHITE, right_eye, eye_radius)
            pygame.draw.circle(self.screen, BLACK, right_eye, eye_radius - 1)
            pygame.draw.circle(self.screen, WHITE, (right_eye[0] - 1, right_eye[1] - 1), 1)  # Highlight
        
        # Vẽ particles
        self.draw_particles()
        
        # Vẽ UI
        self.draw_ui()

        # Draw dialogue overlay last
        if self.dialogue_active:
            self.draw_dialogue()
        # Draw bio panel on top if active
        if self.bio_active:
            self.draw_bio_panel()
        # Draw algorithm menu if active
        if self.menu_active:
            self.draw_algorithm_menu()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # Vẽ thông tin cơ bản ở góc trên (không che map)
        # Score nhanh ở góc trên trái
        score_text = self.small_font.render(f"SCORE: {self.pacman.score:06d}", True, UI_ACCENT)
        score_shadow = self.small_font.render(f"SCORE: {self.pacman.score:06d}", True, BLACK)
        self.screen.blit(score_shadow, (12, 12))
        self.screen.blit(score_text, (10, 10))
        
        # Lives ở góc trên phải
        lives_text = self.small_font.render(f"LIVES: {self.pacman.lives}", True, UI_TEXT)
        lives_shadow = self.small_font.render(f"LIVES: {self.pacman.lives}", True, BLACK)
        self.screen.blit(lives_shadow, (WINDOW_WIDTH - 100, 12))
        self.screen.blit(lives_text, (WINDOW_WIDTH - 102, 10))
        
        # AI Algorithm và Level ở góc trên giữa
        algorithm_text = self.small_font.render(f"AI: {self.pacman.algorithm.value}", True, UI_TEXT)
        algorithm_shadow = self.small_font.render(f"AI: {self.pacman.algorithm.value}", True, BLACK)
        text_rect = algorithm_text.get_rect(center=(WINDOW_WIDTH // 2, 15))
        self.screen.blit(algorithm_shadow, (text_rect.x + 1, text_rect.y + 1))
        self.screen.blit(algorithm_text, text_rect)
        
        # Level
        level_text = self.small_font.render(f"LEVEL: {self.level}", True, UI_ACCENT)
        level_shadow = self.small_font.render(f"LEVEL: {self.level}", True, BLACK)
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, 35))
        self.screen.blit(level_shadow, (level_rect.x + 1, level_rect.y + 1))
        self.screen.blit(level_text, level_rect)
        
        # Vẽ trái tim cho lives ở góc trên phải
        try:
            for i in range(self.pacman.lives):
                heart_x = WINDOW_WIDTH - 80 + i * 20
                heart_y = 35
                pygame.draw.circle(self.screen, RED, (heart_x, heart_y), 6)
                pygame.draw.circle(self.screen, RED, (heart_x + 6, heart_y), 6)
                pygame.draw.polygon(self.screen, RED, [(heart_x - 6, heart_y), (heart_x + 12, heart_y), (heart_x + 3, heart_y + 8)])
        except:
            # Fallback: vẽ trái tim đơn giản
            for i in range(self.pacman.lives):
                heart_x = WINDOW_WIDTH - 80 + i * 20
                heart_y = 35
                pygame.draw.circle(self.screen, RED, (heart_x, heart_y), 4)
        
        # Controls ở góc dưới phải (không che map)
        sound_status = "ON" if self.sound_manager.sound_enabled else "OFF"
        controls = [
            "M: AI Menu",
            "SPACE: Pause",
            "R: Restart", 
            f"S: Sound {sound_status}"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.tiny_font.render(control, True, UI_TEXT)
            control_shadow = self.tiny_font.render(control, True, BLACK)
            y_pos = WINDOW_HEIGHT - 60 + i * 18
            x_pos = WINDOW_WIDTH - 120
            self.screen.blit(control_shadow, (x_pos + 1, y_pos + 1))
            self.screen.blit(control_text, (x_pos, y_pos))
        
        # Game over overlay
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Game over text với hiệu ứng
            game_over_text = self.title_font.render("GAME OVER", True, UI_ACCENT)
            game_over_shadow = self.title_font.render("GAME OVER", True, BLACK)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
            self.screen.blit(game_over_shadow, (text_rect.x + 2, text_rect.y + 2))
            self.screen.blit(game_over_text, text_rect)
            
            # Final score
            score_text = self.font.render(f"Final Score: {self.pacman.score}", True, WHITE)
            score_shadow = self.font.render(f"Final Score: {self.pacman.score}", True, BLACK)
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            self.screen.blit(score_shadow, (score_rect.x + 1, score_rect.y + 1))
            self.screen.blit(score_text, score_rect)
            
            # High scores
            high_score_text = self.small_font.render("HIGH SCORES:", True, UI_ACCENT)
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(high_score_text, high_score_rect)
            
            # Top 3 scores
            for i, score in enumerate(self.high_scores[:3]):
                if score > 0:
                    score_display = self.tiny_font.render(f"{i+1}. {score:06d}", True, UI_TEXT)
                    score_display_rect = score_display.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40 + i * 20))
                    self.screen.blit(score_display, score_display_rect)
            
            restart_text = self.font.render("Press R to Restart", True, UI_TEXT)
            restart_shadow = self.font.render("Press R to Restart", True, BLACK)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 120))
            self.screen.blit(restart_shadow, (restart_rect.x + 2, restart_rect.y + 2))
            self.screen.blit(restart_text, restart_rect)
        
        # Paused overlay
        if self.paused:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(100)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.title_font.render("PAUSED", True, UI_ACCENT)
            pause_shadow = self.title_font.render("PAUSED", True, BLACK)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_shadow, (text_rect.x + 2, text_rect.y + 2))
            self.screen.blit(pause_text, text_rect)

    def draw_dialogue(self):
        """Render dialogue box with speaker and text."""
        if not self.current_dialogue_key:
            return
        lines = self.dialogue_scripts.get(self.current_dialogue_key, [])
        if not lines:
            return
        line = lines[self.dialogue_index]
        speaker = line.get("speaker", "")
        text = line.get("text", "")

        # Dim screen slightly
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(140)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Avatar + Dialogue panel layout
        panel_height = 180
        panel_rect = pygame.Rect(40, WINDOW_HEIGHT - panel_height - 30, WINDOW_WIDTH - 80, panel_height)
        pygame.draw.rect(self.screen, UI_BACKGROUND, panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, UI_BORDER, panel_rect, width=2, border_radius=12)

        # Draw simple avatar for speaker
        avatar_rect = pygame.Rect(panel_rect.x + 16, panel_rect.y + 16, 120, panel_rect.height - 32)
        pygame.draw.rect(self.screen, DARK_GRAY, avatar_rect, border_radius=8)
        self._draw_avatar(speaker, avatar_rect)

        # Speaker
        speaker_surf = self.small_font.render(speaker, True, UI_ACCENT)
        self.screen.blit(speaker_surf, (avatar_rect.right + 16, panel_rect.y + 16))

        # Text wrapping
        def wrap_text(font, content, max_width):
            words = content.split(" ")
            lines_acc = []
            current = ""
            for w in words:
                test = (current + (" " if current else "") + w)
                if font.size(test)[0] <= max_width:
                    current = test
                else:
                    if current:
                        lines_acc.append(current)
                    current = w
            if current:
                lines_acc.append(current)
            return lines_acc

        text_max_width = panel_rect.width - (avatar_rect.width + 16 + 24)
        text_lines = wrap_text(self.font, text, text_max_width)
        for i, t in enumerate(text_lines[:3]):
            t_surf = self.font.render(t, True, UI_TEXT)
            self.screen.blit(t_surf, (avatar_rect.right + 16, panel_rect.y + 52 + i * 28))

        # Hint
        hint = "[Nhan SPACE de tiep]"
        hint_surf = self.tiny_font.render(hint, True, LIGHT_GRAY)
        hint_rect = hint_surf.get_rect(right=panel_rect.right - 16, bottom=panel_rect.bottom - 10)
        self.screen.blit(hint_surf, hint_rect)

    def draw_bio_panel(self):
        """Render an intro info panel about Pac-Man and the mission (ASCII, khong dau)."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        panel_w, panel_h = int(WINDOW_WIDTH * 0.85), int(WINDOW_HEIGHT * 0.7)
        panel_rect = pygame.Rect((WINDOW_WIDTH - panel_w)//2, (WINDOW_HEIGHT - panel_h)//2, panel_w, panel_h)
        pygame.draw.rect(self.screen, UI_BACKGROUND, panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, UI_BORDER, panel_rect, width=2, border_radius=12)

        # Title
        title = "Ho so nhan vat: PAC MAN"
        t_surf = self.title_font.render(title, True, UI_ACCENT)
        t_shadow = self.title_font.render(title, True, BLACK)
        t_rect = t_surf.get_rect(center=(panel_rect.centerx, panel_rect.y + 40))
        self.screen.blit(t_shadow, (t_rect.x + 2, t_rect.y + 2))
        self.screen.blit(t_surf, t_rect)

        # Body text (wrapped)
        lines = [
            "Pac Man: ky su hang khong, nhay ben, lanh tri.",
            "Bo canh: Tram khong gian Neo Labyrinth sau su co hat nhan.",
            "Ly do mac ket: AI SPECTER phong toa, phat hanh ghost truy sat.",
            "Muc tieu: Thu thap cherry kich hoat suc manh, an dot, song sot,",
            "mo lai he thong thoat hiem va roi khoi tram.",
        ]
        y = t_rect.bottom + 20
        for text in lines:
            for row in self._wrap_text(self.font, text, panel_rect.width - 60):
                row_surf = self.font.render(row, True, UI_TEXT)
                self.screen.blit(row_surf, (panel_rect.x + 30, y))
                y += 28

        hint = "[Nhan I hoac SPACE de dong]"
        hint_surf = self.small_font.render(hint, True, LIGHT_GRAY)
        hint_rect = hint_surf.get_rect(center=(panel_rect.centerx, panel_rect.bottom - 30))
        self.screen.blit(hint_surf, hint_rect)

    def _wrap_text(self, font, content, max_width):
        words = content.split(" ")
        lines_acc = []
        current = ""
        for w in words:
            test = (current + (" " if current else "") + w)
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines_acc.append(current)
                current = w
        if current:
            lines_acc.append(current)
        return lines_acc

    def _draw_avatar(self, speaker, rect):
        """Draw a minimal avatar for the speaker using shapes/colors."""
        # Background highlight
        pygame.draw.rect(self.screen, (30, 30, 60), rect, border_radius=8)

        center = (rect.x + rect.width // 2, rect.y + rect.height // 2)
        if speaker.upper().startswith("PAC"):
            # Pac-Man avatar
            radius = min(rect.width, rect.height) // 3
            main_color = YELLOW
            pygame.draw.circle(self.screen, (0, 0, 0), (center[0] + 2, center[1] + 2), radius)
            pygame.draw.circle(self.screen, main_color, center, radius)
            # mouth
            start_angle = math.radians(-30)
            end_angle = math.radians(30)
            mouth_points = [center]
            for angle in [start_angle, end_angle]:
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                mouth_points.append((x, y))
            if len(mouth_points) >= 3:
                pygame.draw.polygon(self.screen, (0, 0, 0), mouth_points)
            # eye
            pygame.draw.circle(self.screen, BLACK, (center[0] + 6, center[1] - 6), 3)
        elif speaker.upper().startswith("SPEC"):
            # SPECTER avatar (AI core)
            pygame.draw.rect(self.screen, LIGHT_BLUE, pygame.Rect(center[0] - 24, center[1] - 24, 48, 48), border_radius=6)
            pygame.draw.rect(self.screen, BLUE, pygame.Rect(center[0] - 18, center[1] - 18, 36, 36), border_radius=6)
            for i in range(4):
                pygame.draw.circle(self.screen, UI_ACCENT, (center[0] - 12 + i * 8, center[1]), 3)
        elif speaker.upper().startswith("BLIN") or speaker.upper().startswith("PINK") or speaker.upper().startswith("INKY") or speaker.upper().startswith("CLY"):
            # Ghost avatar
            ghost_color = RED if speaker.upper().startswith("BLIN") else PINK if speaker.upper().startswith("PINK") else BLUE if speaker.upper().startswith("INKY") else ORANGE
            body_rect = pygame.Rect(center[0] - 26, center[1] - 20, 52, 40)
            pygame.draw.ellipse(self.screen, ghost_color, body_rect)
            # teeth
            for i in range(0, 52, 8):
                x1 = body_rect.x + i
                y1 = body_rect.bottom - 2
                x2 = x1 + 4
                y2 = y1 + 6
                x3 = x1 + 8
                y3 = y1 - 2
                if x3 <= body_rect.right:
                    pygame.draw.polygon(self.screen, ghost_color, [(x1, y1), (x2, y2), (x3, y3)])
            # eyes
            pygame.draw.circle(self.screen, WHITE, (center[0] - 8, center[1] - 6), 5)
            pygame.draw.circle(self.screen, BLACK, (center[0] - 8, center[1] - 6), 3)
            pygame.draw.circle(self.screen, WHITE, (center[0] + 8, center[1] - 6), 5)
            pygame.draw.circle(self.screen, BLACK, (center[0] + 8, center[1] - 6), 3)
        else:
            # Generic log/avatar
            pygame.draw.circle(self.screen, GRAY, center, min(rect.width, rect.height) // 6)
    
    def handle_menu_click(self, pos):
        """Handle mouse click on algorithm menu."""
        menu_width = 450
        item_height = 28
        title_height = 50
        footer_height = 35
        content_height = len(self.algorithms) * item_height
        menu_height = content_height + title_height + footer_height
        menu_x = (WINDOW_WIDTH - menu_width) // 2
        menu_y = (WINDOW_HEIGHT - menu_height) // 2
        
        # Check if clicked inside menu
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        if not menu_rect.collidepoint(pos):
            # Clicked outside menu - close it
            self.menu_active = False
            self.paused = False
            return
        
        # Check algorithm items
        item_y = menu_y + title_height
        for i, algorithm in enumerate(self.algorithms):
            item_rect = pygame.Rect(menu_x + 15, item_y + i * item_height, menu_width - 30, item_height - 3)
            if item_rect.collidepoint(pos):
                # Selected algorithm
                self.current_algorithm = i
                self.pacman.set_algorithm(self.algorithms[self.current_algorithm])
                print(f"Selected algorithm: {self.algorithms[self.current_algorithm].value}")
                self.menu_active = False
                self.paused = False
                self.sound_manager.play_sound('eat_dot')
                break
    
    def handle_menu_hover(self, pos):
        """Handle mouse hover on algorithm menu."""
        menu_width = 450
        item_height = 28
        title_height = 50
        footer_height = 35
        content_height = len(self.algorithms) * item_height
        menu_height = content_height + title_height + footer_height
        menu_x = (WINDOW_WIDTH - menu_width) // 2
        menu_y = (WINDOW_HEIGHT - menu_height) // 2
        
        # Check algorithm items
        item_y = menu_y + title_height
        self.menu_hover_index = -1
        for i, algorithm in enumerate(self.algorithms):
            item_rect = pygame.Rect(menu_x + 15, item_y + i * item_height, menu_width - 30, item_height - 3)
            if item_rect.collidepoint(pos):
                self.menu_hover_index = i
                break
    
    def draw_algorithm_menu(self):
        """Draw algorithm selection menu."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Menu panel - giảm khoảng cách để chứa đủ tất cả thuật toán
        menu_width = 450
        item_height = 28  # Giảm từ 35 xuống 28 để chứa nhiều hơn
        title_height = 50
        footer_height = 35
        content_height = len(self.algorithms) * item_height
        menu_height = content_height + title_height + footer_height
        menu_x = (WINDOW_WIDTH - menu_width) // 2
        menu_y = (WINDOW_HEIGHT - menu_height) // 2
        
        # Panel background with glow
        glow_rect = pygame.Rect(menu_x - 4, menu_y - 4, menu_width + 8, menu_height + 8)
        pygame.draw.rect(self.screen, UI_ACCENT, glow_rect, border_radius=12)
        
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, (25, 25, 50), menu_rect, border_radius=10)
        pygame.draw.rect(self.screen, UI_ACCENT, menu_rect, 2, border_radius=10)
        
        # Title
        title = "CHON THUAT TOAN AI"
        title_surf = self.title_font.render(title, True, UI_ACCENT)
        title_shadow = self.title_font.render(title, True, BLACK)
        title_rect = title_surf.get_rect(center=(menu_x + menu_width // 2, menu_y + 25))
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title_surf, title_rect)
        
        # Algorithm list - không cần clipping vì menu đủ lớn
        item_y = menu_y + title_height
        
        for i, algorithm in enumerate(self.algorithms):
            current_item_y = item_y + i * item_height
            item_rect = pygame.Rect(menu_x + 15, current_item_y, menu_width - 30, item_height - 3)
            
        for i, algorithm in enumerate(self.algorithms):
            current_item_y = item_y + i * item_height
            item_rect = pygame.Rect(menu_x + 15, current_item_y, menu_width - 30, item_height - 3)
            
            # Highlight current or hovered
            is_current = (i == self.current_algorithm)
            is_hovered = (i == self.menu_hover_index)
            
            if is_current:
                # Current algorithm - highlight with accent color
                pygame.draw.rect(self.screen, UI_ACCENT, item_rect, border_radius=5)
                text_color = BLACK
            elif is_hovered:
                # Hovered - lighter highlight
                pygame.draw.rect(self.screen, (60, 80, 120), item_rect, border_radius=5)
                text_color = WHITE
            else:
                # Normal
                pygame.draw.rect(self.screen, (40, 40, 70), item_rect, border_radius=5)
                text_color = UI_TEXT
            
            # Algorithm name
            alg_text = self.small_font.render(algorithm.value, True, text_color)
            alg_rect = alg_text.get_rect(midleft=(item_rect.x + 12, item_rect.centery))
            self.screen.blit(alg_text, alg_rect)
            
            # Current indicator
            if is_current:
                indicator = "◄"
                ind_surf = self.small_font.render(indicator, True, BLACK)
                ind_rect = ind_surf.get_rect(midright=(item_rect.right - 12, item_rect.centery))
                self.screen.blit(ind_surf, ind_rect)
        
        # Instructions
        hint = "[M/ESC: Dong | Click de chon]"
        hint_surf = self.tiny_font.render(hint, True, LIGHT_GRAY)
        hint_rect = hint_surf.get_rect(center=(menu_x + menu_width // 2, menu_y + menu_height - 18))
        self.screen.blit(hint_surf, hint_rect)
    
    def restart_game(self):
        self.maze = self.create_maze()
        self.pacman = PacmanAI(1, 1)
        self.pacman.set_algorithm(self.algorithms[self.current_algorithm])
        house_cx, house_cy = MAZE_WIDTH // 2, MAZE_HEIGHT // 2
        ghost_colors = [RED, PINK, BLUE, ORANGE]
        ghost_positions = [
            (house_cx, house_cy),
            (house_cx - 1, house_cy),
            (house_cx + 1, house_cy),
            (house_cx, house_cy + 1)
        ]
        self.ghosts = [Ghost(x, y, ghost_colors[i]) for i, (x, y) in enumerate(ghost_positions)]
        self.game_over = False
        self.paused = False
        self.level_complete = False
        self.level = 1
        self.particle_effects = []
        self.sound_manager.play_sound('pause')
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS để dễ quan sát AI
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
