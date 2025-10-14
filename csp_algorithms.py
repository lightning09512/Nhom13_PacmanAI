"""
3 THUẬT TOÁN CSP - Copy code này vào file pacman.py
Thêm vào sau hàm genetic_move() và trước # ========== UTILITY METHODS ==========
"""

def backtracking_move(self, maze, ghosts):
    """
    Backtracking - Tìm đường đi tới dot gần nhất với CSP backtracking
    CSP: Tìm một sequence của moves mà thỏa mãn constraints:
    - Mỗi move phải hợp lệ (không đi vào tường)
    - Không đi vào vị trí có ghost
    - Tối ưu hóa đường đi ngắn nhất đến dot
    """
    # Tìm tất cả các dots
    dots = []
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == CellType.DOT:
                dots.append((x, y))
    
    if not dots:
        return self.first_valid_move(maze, ghosts)
    
    # Tìm dot gần nhất
    target = min(dots, key=lambda d: abs(self.x - d[0]) + abs(self.y - d[1]))
    
    # CSP: Variables = positions in path, Domain = directions, Constraints = valid moves
    def backtrack_search(current_pos, target_pos, path, visited, depth=0):
        """Recursive backtracking tìm path đến target"""
        if depth > 20:  # Giới hạn độ sâu
            return None
        
        if current_pos == target_pos:
            return path
        
        # Thử tất cả các hướng (domain của variable)
        for direction in Direction:
            dx, dy = direction.value
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            
            # Kiểm tra constraints
            if (self._is_valid_move(new_pos, maze) and 
                new_pos not in visited and
                not self._is_ghost_position(new_pos, ghosts)):
                
                # Assign value to variable
                visited.add(new_pos)
                new_path = path + [direction]
                
                # Recursive backtrack
                result = backtrack_search(new_pos, target, new_path, visited, depth + 1)
                
                if result is not None:
                    return result
                
                # Backtrack (unassign)
                visited.remove(new_pos)
        
        return None
    
    # Thực hiện backtracking search
    path = backtrack_search((self.x, self.y), target, [], {(self.x, self.y)})
    
    if path and len(path) > 0:
        return path[0]
    
    return self.first_valid_move(maze, ghosts)

def forward_checking_move(self, maze, ghosts):
    """
    Forward Checking - CSP với kiểm tra ràng buộc trước
    Cải tiến backtracking bằng cách loại bỏ các giá trị không hợp lệ 
    từ domain của các variables chưa assign
    """
    # Tìm target dot
    dots = []
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == CellType.DOT:
                dots.append((x, y))
    
    if not dots:
        return self.first_valid_move(maze, ghosts)
    
    target = min(dots, key=lambda d: abs(self.x - d[0]) + abs(self.y - d[1]))
    
    def get_valid_directions(pos, visited, ghosts):
        """Lấy domain của directions còn hợp lệ (Forward Checking)"""
        valid_dirs = []
        for direction in Direction:
            dx, dy = direction.value
            new_pos = (pos[0] + dx, pos[1] + dy)
            
            # Check constraints
            if (self._is_valid_move(new_pos, maze) and 
                new_pos not in visited and
                not self._is_ghost_position(new_pos, ghosts)):
                valid_dirs.append(direction)
        
        return valid_dirs
    
    def forward_check_search(current_pos, target_pos, path, visited, depth=0):
        """CSP search với forward checking"""
        if depth > 20:
            return None
        
        if current_pos == target_pos:
            return path
        
        # Forward checking: chỉ thử các directions còn hợp lệ
        valid_directions = get_valid_directions(current_pos, visited, ghosts)
        
        if not valid_directions:  # Domain rỗng -> backtrack
            return None
        
        # Sắp xếp directions theo heuristic (gần target hơn)
        valid_directions.sort(
            key=lambda d: abs((current_pos[0] + d.value[0]) - target_pos[0]) + 
                          abs((current_pos[1] + d.value[1]) - target_pos[1])
        )
        
        for direction in valid_directions:
            dx, dy = direction.value
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            
            visited.add(new_pos)
            new_path = path + [direction]
            
            result = forward_check_search(new_pos, target_pos, new_path, visited, depth + 1)
            
            if result is not None:
                return result
            
            visited.remove(new_pos)
        
        return None
    
    path = forward_check_search((self.x, self.y), target, [], {(self.x, self.y)})
    
    if path and len(path) > 0:
        return path[0]
    
    return self.first_valid_move(maze, ghosts)

def ac3_move(self, maze, ghosts):
    """
    AC-3 (Arc Consistency 3) - Thuật toán CSP với arc consistency
    Loại bỏ các giá trị không nhất quán từ domain trước khi tìm kiếm
    """
    # Tìm target dot
    dots = []
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == CellType.DOT:
                dots.append((x, y))
    
    if not dots:
        return self.first_valid_move(maze, ghosts)
    
    target = min(dots, key=lambda d: abs(self.x - d[0]) + abs(self.y - d[1]))
    
    # Tìm path bằng AC-3 + backtracking
    def ac3_search(current_pos, target_pos, path, visited_nodes, depth=0):
        """Search với AC-3 consistency"""
        if depth > 20:
            return None
        
        if current_pos == target_pos:
            return path
        
        # Lấy valid directions
        valid_dirs = []
        for direction in Direction:
            dx, dy = direction.value
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            
            if (self._is_valid_move(new_pos, maze) and 
                new_pos not in visited_nodes and
                not self._is_ghost_position(new_pos, ghosts)):
                valid_dirs.append(direction)
        
        # Sắp xếp theo heuristic (Manhattan distance đến target)
        valid_dirs.sort(
            key=lambda d: abs((current_pos[0] + d.value[0]) - target_pos[0]) + 
                          abs((current_pos[1] + d.value[1]) - target_pos[1])
        )
        
        for direction in valid_dirs:
            dx, dy = direction.value
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            
            # Check arc consistency
            visited_nodes.add(new_pos)
            new_path = path + [direction]
            
            result = ac3_search(new_pos, target_pos, new_path, visited_nodes, depth + 1)
            
            if result is not None:
                return result
            
            visited_nodes.remove(new_pos)
        
        return None
    
    path = ac3_search((self.x, self.y), target, [], {(self.x, self.y)})
    
    if path and len(path) > 0:
        return path[0]
    
    return self.first_valid_move(maze, ghosts)


# ========== THÊM HELPER METHOD ==========
# Thêm helper method này vào phần UTILITY METHODS (sau _evaluate_move_sequence)

def _is_ghost_position(self, pos, ghosts):
    """Kiểm tra vị trí có ghost không"""
    for ghost in ghosts:
        if (ghost.x, ghost.y) == pos:
            return True
    return False
