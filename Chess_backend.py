# Base class for all chess pieces
class ChessPiece:
    def __init__(self, name, color, position):
        self.name = name  # Name of the piece (e.g., "pawn", "rook")
        self.color = color  # Color of the piece ('white' or 'black')
        self.position = position  # Current position of the piece as a tuple (x, y)
        self.move_count = 0  # Number of times the piece has moved

    def move(self, new_position):
        """Updates the piece's position and increments move_count."""
        self.position = new_position
        self.move_count += 1


# Pawn class inherits from ChessPiece
class Pawn(ChessPiece):
    def get_valid_moves(self, board):
        valid_moves = []
        direction = -1 if self.color == 'white' else 1  # Pawns move in opposite directions based on color
        x, y = self.position

        # Move forward
        if board.is_empty((x, y + direction)):
            valid_moves.append((x, y + direction))
            # Move two squares on first move
            if self.move_count == 0 and board.is_empty((x, y + 2 * direction)):
                valid_moves.append((x, y + 2 * direction))

        # Capture diagonally
        for dx in [-1, 1]:
            if board.is_enemy((x + dx, y + direction), self.color):
                valid_moves.append((x + dx, y + direction))

        return valid_moves


# Rook class inherits from ChessPiece
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


# Knight class inherits from ChessPiece
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


# Bishop class inherits from ChessPiece
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


# Queen class inherits from ChessPiece
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


# King class inherits from ChessPiece
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

        return valid_moves


# Board class to manage the chessboard and pieces
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  # 8x8 grid representing the board

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
        """Moves a piece from one position to another if the move is valid."""
        from_x, from_y = from_position
        to_x, to_y = to_position
        piece = self.grid[from_x][from_y]
        if piece and to_position in piece.get_valid_moves(self):
            self.grid[to_x][to_y] = piece
            self.grid[from_x][from_y] = None
            piece.move(to_position)
            return True
        return False

    def display(self):
        """Prints the board in a simple text format."""
        for y in range(8):
            row = []
            for x in range(8):
                piece = self.grid[x][y]
                if piece:
                    row.append(f"{piece.name[0].upper()}{piece.color[0]}")  # Display piece name and color
                else:
                    row.append("..")  # Display empty squares as ".."
            print(" ".join(row))


# Initialize the board and place pieces
board = Board()
board.place_piece(Pawn("pawn", "white", (1, 1)), (1, 1))
board.place_piece(Rook("rook", "white", (0, 0)), (0, 0))
board.place_piece(Knight("knight", "white", (1, 0)), (1, 0))
board.place_piece(Bishop("bishop", "white", (2, 0)), (2, 0))
board.place_piece(Queen("queen", "white", (3, 0)), (3, 0))
board.place_piece(King("king", "white", (4, 0)), (4, 0))
board.place_piece(Pawn("pawn", "black", (1, 6)), (1, 6))


# Simple text-based interface
def play_game():
    while True:
        board.display()
        move_from = input("Enter the piece's current position (x y): ").split()
        move_to = input("Enter the new position (x y): ").split()

        if not move_from or not move_to:
            print("Invalid input. Try again.")
            continue

        from_pos = tuple(map(int, move_from))
        to_pos = tuple(map(int, move_to))

        if board.move_piece(from_pos, to_pos):
            print("Move successful!")
        else:
            print("Invalid move. Try again.")


if __name__ == "__main__":
    play_game()
