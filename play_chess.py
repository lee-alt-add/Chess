import string
from Games import Chess

# Function to extract, organize and generate the board.
def generate_board(board):

    chess = Chess('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1')
    
    chess.Move()

    return

generate_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1')

# def game_progress(board):

#     # Board attributes
#     who_moves = board.split()[1] # Black or White move
#     can_castle = board.split()[2] # Castle values
#     en_passant = board.split()[3]# En-passant value
#     half_move = int(board.split()[4]) # Halfmove clock
#     full_move = int(board.split()[5]) # Fullmove clock
#     print()


#     # White or Black to move?
#     if "w" in who_moves:
#         print("White to move")
#     elif "b" in who_moves:
#         print("Black to move")
    
    

#     # Castling Black
#     if "k" in can_castle and "q" in can_castle:
#         print('Black can castle on both sides')
#     elif "k" in can_castle:
#         print('Black can castle on king')
#     elif "q" in can_castle:
#         print('Black can castle on queen')

#     # Castling White
#     if "K" in can_castle and "Q" in can_castle:
#         print('White can castle on both sides')
#     elif "K" in can_castle:
#         print('White can castle on king')
#     elif "Q" in can_castle:
#         print('White can castle on queen')

#     # No Castle move
#     if '-' in can_castle:
#         print('Both sides cannot castle')

#     # En-passant
#     if "-" in en_passant:
#         print("No en passant square")
#     else:
#         print("en passant square available")


#     #Halfmove
#     print(f"Halfmove clock: {half_move}")

#     #Fullmove
#     print(f"Fullmove number: {full_move}")

# def viewfen(board):
#     #board = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1'
    
#     generate_board(board)
#     game_progress(board)
    

#     return


# if __name__ == "__main__":
#     import sys
#     viewfen(sys.argv[1])
