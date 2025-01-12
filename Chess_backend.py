class ChessPiece:
    def __init__(self, name, color, position):
        self.name = name  # Name of the piece (e.g., "pawn", "rook")
        self.color = color  # Color of the piece ('white' or 'black')
        self.position = position  # Current position of the piece as a tuple (x, y)
        self.move_count = 0  # Number of times the piece has moved

    def get_valid_moves(self, board):
        """Returns a list of valid moves for the piece based on the board state."""
        raise NotImplementedError("Subclasses must implement this method")

    def move(self, new_position):
        """Updates the piece's position and increments move_count."""
        self.position = new_position
        self.move_count += 1


class Pawn(ChessPiece):
    def get_valid_moves(self, board):
        valid_moves = []
        direction = -1 if self.color == 'white' else 1  # White moves up, black moves down
        x, y = self.position

        # Move forward
        new_y = y + direction
        if board.is_within_bounds((x, new_y)) and board.is_empty((x, new_y)):
            valid_moves.append((x, new_y))
            # Move two squares on first move
            if self.move_count == 0:
                new_y2 = y + 2 * direction
                if board.is_within_bounds((x, new_y2)) and board.is_empty((x, new_y2)):
                    valid_moves.append((x, new_y2))

        # Capture diagonally
        for dx in [-1, 1]:
            new_x, new_y = x + dx, y + direction
            if board.is_within_bounds((new_x, new_y)):
                # Regular capture
                if board.is_enemy((new_x, new_y), self.color):
                    valid_moves.append((new_x, new_y))
                # En passant
                else:
                    adjacent_pawn = board.grid[new_x][y]
                    if isinstance(adjacent_pawn, Pawn) and adjacent_pawn.move_count == 1:
                        valid_moves.append((new_x, new_y))

        return valid_moves
    
    # Pawn promotion
    def promote(self, board):
        """Promotes the pawn to a new piece."""
        promotion_pieces = {
            'q': Queen,
            'r': Rook,
            'b': Bishop,
            'n': Knight,
        }

        print("Pawn promotion! Choose a piece to promote to:")
        print("q - Queen, r - Rook, b - Bishop, n - Knight")
        choice = input("Enter your choice: ").lower()

        if choice in promotion_pieces:
            new_piece = promotion_pieces[choice](choice.upper(), self.color, self.position)
            board.place_piece(new_piece, self.position)
        else:
            print("Invalid choice. Promoting to Queen by default.")
            new_piece = Queen(self.name, self.color, self.position)
            board.place_piece(new_piece, self.position)


class Rook(ChessPiece):
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.position

        # Horizontal and vertical moves
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, 8):  # Rooks can move up to 7 squares in any direction
                new_x, new_y = x + i * dx, y + i * dy
                if not board.is_within_bounds((new_x, new_y)):
                    break  # Stop if the move is outside the board
                if board.is_empty((new_x, new_y)):
                    valid_moves.append((new_x, new_y))
                elif board.is_enemy((new_x, new_y), self.color):
                    valid_moves.append((new_x, new_y))
                    break  # Stop if an enemy piece is encountered
                else:
                    break  # Stop if a friendly piece is encountered

        return valid_moves


class Knight(ChessPiece):
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.position

        # All possible L-shaped moves
        moves = [
            (x + 2, y + 1), (x + 2, y - 1),
            (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2),
            (x - 1, y + 2), (x - 1, y - 2),
        ]

        for new_x, new_y in moves:
            if board.is_within_bounds((new_x, new_y)) and (
                board.is_empty((new_x, new_y)) or board.is_enemy((new_x, new_y), self.color)
            ):
                valid_moves.append((new_x, new_y))

        return valid_moves


class Bishop(ChessPiece):
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.position

        # Diagonal moves
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):  # Bishops can move up to 7 squares diagonally
                new_x, new_y = x + i * dx, y + i * dy
                if not board.is_within_bounds((new_x, new_y)):
                    break  # Stop if the move is outside the board
                if board.is_empty((new_x, new_y)):
                    valid_moves.append((new_x, new_y))
                elif board.is_enemy((new_x, new_y), self.color):
                    valid_moves.append((new_x, new_y))
                    break  # Stop if an enemy piece is encountered
                else:
                    break  # Stop if a friendly piece is encountered

        return valid_moves


class Queen(ChessPiece):
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.position

        # Combine rook and bishop moves (horizontal, vertical, and diagonal)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):  # Queens can move up to 7 squares in any direction
                new_x, new_y = x + i * dx, y + i * dy
                if not board.is_within_bounds((new_x, new_y)):
                    break  # Stop if the move is outside the board
                if board.is_empty((new_x, new_y)):
                    valid_moves.append((new_x, new_y))
                elif board.is_enemy((new_x, new_y), self.color):
                    valid_moves.append((new_x, new_y))
                    break  # Stop if an enemy piece is encountered
                else:
                    break  # Stop if a friendly piece is encountered

        return valid_moves


class King(ChessPiece):
    def get_valid_moves(self, board):
        valid_moves = []
        x, y = self.position

        # All adjacent squares (one square in any direction)
        moves = [
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1),
        ]

        for new_x, new_y in moves:
            if board.is_within_bounds((new_x, new_y)) and (
                board.is_empty((new_x, new_y)) or board.is_enemy((new_x, new_y), self.color)
            ):
                valid_moves.append((new_x, new_y))

        # Castling (optional, can be implemented later)

        return valid_moves


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  # 8x8 grid
        self.current_turn = 'white'  # Track whose turn it is

    def is_empty(self, position):
        """Checks if a position on the board is empty."""
        x, y = position
        return self.grid[x][y] is None

    def is_enemy(self, position, color):
        """Checks if a position on the board is occupied by an enemy piece."""
        x, y = position
        piece = self.grid[x][y]
        return piece is not None and piece.color != color

    def is_within_bounds(self, position):
        """Checks if a position is within the bounds of the board."""
        x, y = position
        return 0 <= x < 8 and 0 <= y < 8

    def place_piece(self, piece, position):
        """Places a piece on the board at the specified position."""
        x, y = position
        self.grid[x][y] = piece

    def move_piece(self, from_position, to_position):
        from_x, from_y = from_position
        to_x, to_y = to_position
        piece = self.grid[from_x][from_y]

        if piece and piece.color == self.current_turn:
            valid_moves = piece.get_valid_moves(self)
            if to_position in valid_moves:
                # Move the piece
                self.grid[to_x][to_y] = piece
                self.grid[from_x][from_y] = None
                piece.move(to_position)

                # Handle en passant capture
                if isinstance(piece, Pawn) and abs(to_y - from_y) == 2:
                    # Mark the pawn as eligible for en passant
                    piece.move_count = 1  # Reset move count to indicate it just moved two squares
                elif isinstance(piece, Pawn) and abs(to_x - from_x) == 1 and board.is_empty((to_x, to_y)):
                    # Perform en passant capture
                    captured_pawn_y = to_y - direction
                    self.grid[to_x][captured_pawn_y] = None

                # Check for pawn promotion
                if isinstance(piece, Pawn) and (to_y == 0 or to_y == 7):
                    piece.promote(self)

                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                return True
        return False

    def display(self):
        """Prints the board in a simple text format."""
        for y in range(8):
            row = []
            for x in range(8):
                piece = self.grid[x][y]
                if piece:
                    row.append(f"{piece.name[0].upper()}{piece.color[0]}")
                else:
                    row.append("..")
            print(" ".join(row))


# Initialize the board and place pieces
board = Board()
board.place_piece(Pawn("pawn", "white", (1, 2)), (1, 2))
board.place_piece(Rook("rook", "white", (0, 0)), (0, 0))
board.place_piece(Knight("knight", "white", (1, 0)), (1, 0))
board.place_piece(Bishop("bishop", "white", (2, 0)), (2, 0))
board.place_piece(Queen("queen", "white", (3, 0)), (3, 0))
board.place_piece(King("king", "white", (4, 0)), (4, 0))
board.place_piece(Pawn("pawn", "black", (1, 6)), (1, 6))


# Simple text-based interface
def play_game():
    while True:
        print(f"{board.current_turn.capitalize()}'s turn")
        board.display()
        print("Enter positions as 'x y' (e.g., '1 1').")

        # Get current position of the piece
        move_from = input("Enter the piece's current position (x y): ").split()
        if len(move_from) != 2:
            print("Invalid input. Please enter two numbers.")
            continue

        from_pos = tuple(map(int, move_from))
        if not board.is_within_bounds(from_pos):
            print("Invalid position. Please enter values between 0 and 7.")
            continue

        piece = board.grid[from_pos[0]][from_pos[1]]
        if not piece or piece.color != board.current_turn:
            print("No valid piece at this position.")
            continue

        # Display valid moves for the selected piece
        valid_moves = piece.get_valid_moves(board)
        print(f"Valid moves for {piece.name} at {from_pos}: {valid_moves}")

        # Get new position for the piece
        move_to = input("Enter the new position (x y): ").split()
        if len(move_to) != 2:
            print("Invalid input. Please enter two numbers.")
            continue

        to_pos = tuple(map(int, move_to))
        if not board.is_within_bounds(to_pos):
            print("Invalid position. Please enter values between 0 and 7.")
            continue

        # Attempt to move the piece
        if board.move_piece(from_pos, to_pos):
            print("Move successful!")
        else:
            print("Invalid move. Try again.")


if __name__ == "__main__":
    play_game()
