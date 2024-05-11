def is_valid_queen(self, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Calculate the row and column differences
    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)
    # Check if the movement is along a straight line (horizontal, vertical, or diagonal)
    if (row_diff == 0 or col_diff == 0 or row_diff == col_diff):
        # Check for obstructions along the path
        if row_diff == 0:  # Horizontal movement
            direction = 1 if end_col > start_col else -1
            for col in range(start_col + direction, end_col, direction):
                if self.board[start_row][col]:
                    return False
        elif col_diff == 0:  # Vertical movement
            direction = 1 if end_row > start_row else -1
            for row in range(start_row + direction, end_row, direction):
                if self.board[row][start_col]:
                    return False
        else:  # Diagonal movement
            row_direction = 1 if end_row > start_row else -1
            col_direction = 1 if end_col > start_col else -1
            for i in range(1, row_diff):
                row = start_row + i * row_direction
                col = start_col + i * col_direction
                if self.board[row][col]:
                    return False
        # No obstructions, movement is valid
        return True
    
    # Invalid movement
    return False


def is_valid_king(self, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    # Calculate the row and column differences
    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)
    # Calculate the row and column differences
    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)
    # Check if the movement is within one square in any direction
    if row_diff <= 1 and col_diff <= 1:
        # Valid movement
        return True

    # Invalid movement
    return False


def is_valid_pawn(self, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Determine the direction of movement based on the color of the pawn
    direction = 1 if self.board[start_row][start_col][0] == 'w' else -1

    # Check if the pawn is moving forward
    if start_col == end_col:
        # Check if the pawn is moving one square forward
        if start_row + direction == end_row and not self.board[end_row][end_col]:
            return True
        # Check if the pawn is moving two squares forward on its first move
        if ((start_row == 1 and direction == 1) or (start_row == 6 and direction == -1)) and start_row + 2 * direction == end_row and not self.board[start_row + direction][end_col] and not self.board[end_row][end_col]:
            return True
    # Check if the pawn is capturing diagonally
    elif abs(start_col - end_col) == 1 and start_row + direction == end_row:
        if self.board[end_row][end_col] and self.board[end_row][end_col][0] != self.board[start_row][start_col][0]:
            return True

    # Invalid movement
    return False
