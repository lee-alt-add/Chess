import string

 # Real Chess board referrences
def Chess_Board_with_referrences(new_board):
    moves = {}

    iterator = iter([0,1,2,3,4,5,6,7])
    for alph in "ABCDEFGH":
        i = next(iterator)
        moves[alph] = {
                '8': new_board[0][i],
                '7': new_board[1][i],
                '6': new_board[2][i],
                '5': new_board[3][i],
                '4': new_board[4][i],
                '3': new_board[5][i],
                '2': new_board[6][i],
                '1': new_board[7][i]
        }
    return moves






class Chess():
    """Making a move, e.g. A5, C3, G6"""
    class piece():
        has_moved_before = False
        count = 0
        name = ''

        def __init__(self, name):
            self.name = name


        def get_name(self):
            return self.name

        def get_count(self):
            return self.count

        def move(self):
            self.count += 1
            self.has_moved_before = True

    Board = []
    def __init__(self, board):
        self.board = board
        self.Board = self.board_to_list()


    def board_to_list(self):
        new_board = [] # To store rows
        holder = [] # To store the values in each box
        board = self.board.split()[0] + '/' # Seperates the board values from the rest of the fen string
        
        # Prepare and sort board values by placing in list.
        for letter in board:
            if letter in string.ascii_lowercase or letter in string.ascii_uppercase:
                piece = self.piece(letter)
                holder.append(piece) # Place alphabet values in a list as they are.
            elif letter.isdigit():
                for i in range(int(letter)):
                    piece = self.piece('.')
                    holder.append(piece) # Converts int value to string '.' and place in list.
            else:
                new_board.append(holder) # If the letter is '/' take the list with values and append into new_board list
                holder = [] # Reset list to capture new values
        
        return new_board

    def display_board(self,board):
        for i in range(8):
            print(f"{self.Board[i][0].name} {self.Board[i][1].name} {self.Board[i][2].name} {self.Board[i][3].name} {self.Board[i][4].name} {self.Board[i][5].name} {self.Board[i][6].name} {self.Board[i][7].name}") 

    def Move(self):

        def get_row(move):
            key = {'H':0, 'G':1, 'F':2, 'E':3, 'D':4, 'C':5, 'B':6, 'A':7}
            row = int(key[move[0].upper()])
            return row  # Index of the row

        def get_position(move):
            position = int(move[1]) - 1
            return position  # Index of box

        def get_object(move):
            return self.Board[get_row(move)][get_position(move)]

        def get_object_name(move):
            return self.Board[get_row(move)][get_position(move)].get_name()   # Name of object that is in the box

        def move_piece(from_move):

            def update_board(from_move, to_move, from_box):
                # Move the piece to new position
                self.Board[get_row(to_move)][get_position(to_move)] = get_object(from_move)
                self.Board[get_row(to_move)][get_position(to_move)].move()

                # Update the box where piece was located
                self.Board[get_row(from_move)][get_position(from_move)] = self.piece('.')

            def move_is_valid(the_object, from_move, to_move):

                def row_count(from_move, to_move):
                    if ord(from_move[0]) > ord(to_move[0]):
                        return ord(from_move[0]) - ord(to_move[0])
                    else:
                        return ord(to_move[0]) - ord(from_move[0])

                def box_count(from_move, to_move):
                    if int(from_move[1]) > int(to_move[1]):
                        return int(from_move[1]) - int(to_move[1])
                    else:
                        return int(to_move[1]) - int(from_move[1])

                def occupant(number, the_object, from_move, to_move):
                    if the_object.name == "B":
                        if ord(from_move[0]) > ord(to_move[0]):
                            return chr(ord(from_move[0]) - number) + str(int(from_move[1]) - number)

                        elif ord(from_move[0]) < ord(to_move[0]):
                            return chr(ord(from_move[0]) + number) + str(int(from_move[1]) + number)

                    elif the_object.name in "RQ":
                        if ord(from_move[0]) > ord(to_move[0]):
                            return chr((ord(from_move[0])) - number) + from_move[1]

                        elif ord(from_move[0]) < ord(to_move[0]):
                            return chr((ord(from_move[0])) + number) + from_move[1]

                        elif int(from_move[1]) > int(to_move[1]):
                            return from_move[0] + str(int(from_move[1]) - number)

                        elif int(from_move[1]) < int(to_move[1]):
                            return from_move[0] + str(int(from_move[1]) + number)


                if the_object.name == 'P':
                    if the_object.has_moved_before == True:
                        if row_count(from_move, to_move) == 1 and box_count(from_move, to_move) == 1: # Forward one move
                            return True
                        return False

                    elif the_object.has_moved_before == False:
                        if row_count(from_move, to_move) in range(1,3) and from_move[1] == to_move[1]: # El pessant
                            return True
                        elif row_count(from_move, to_move) == 1 and box_count(from_move, to_move) == 1: # Up-right
                            return True
                        return False

                elif the_object.name == "R":
                    if the_object.has_moved_before == False or the_object.has_moved_before == True:

                        for i in range(1, row_count(from_move,to_move)):
                            box_occupant = occupant(i, the_object, from_move, to_move)
                            along_route = get_object(box_occupant)
                            if along_route.name in 'RNBKQP':
                                return False

                        if from_move[0] != to_move[0] and from_move[1] != to_move[1]:
                            return False

                        return True

                elif the_object.name == "N":
                    if row_count(from_move, to_move) == 2:
                        if box_count(from_move, to_move) == 1: 
                            return True
                    elif row_count(from_move, to_move) == 1:
                        if box_count(from_move, to_move) == 2:
                            return True
                    return False

                elif the_object.name == "B":
                    if row_count(from_move, to_move) == box_count(from_move, to_move):
                        for i in range(1,row_count(from_move, to_move)):
                            box_occupant = occupant(i, the_object, from_move, to_move)
                            occupant_type = get_object(box_occupant)
                            if occupant_type.name in 'RNBKQP':
                                return False
                        return True

                elif the_object.name == 'Q':

                    # Rouke-like moves
                    if row_count(from_move, to_move) != box_count(from_move, to_move):
                        for i in range(1, row_count(from_move,to_move)):
                            box_occupant = occupant(i, the_object, from_move, to_move)
                            along_route = get_object(box_occupant)
                            if along_route.name in 'RNBKQP':
                                return False

                        if from_move[0] != to_move[0] and from_move[1] != to_move[1]:
                            return False

                        return True

                    # Brook-like moves
                    elif row_count(from_move, to_move) == box_count(from_move, to_move):
                        for i in range(1,row_count(from_move, to_move)):
                            box_occupant = occupant(i, the_object, from_move, to_move)
                            occupant_type = get_object(box_occupant)
                            if occupant_type.name in 'RNBKQP':
                                return False
                        return True



            while True:
                to_move = input("To position?:  ")

                # Get object in from_move
                the_object = get_object(from_move)

                # Get name of object in to_move
                to_box = get_object_name(to_move)

                if the_object.name == "P":
                    if move_is_valid(the_object, from_move, to_move):
                        if to_box in 'rnbkqp.':
                            update_board(from_move, to_move, the_object.name)
                            break
                    else:
                        print("Invalid choice, try again")

                elif the_object.name == "R":
                    if move_is_valid(the_object, from_move, to_move):
                        if to_box in 'rnbkqp.':
                            update_board(from_move, to_move, the_object.name)
                            break
                    else:
                        print("invalid move, try again")

                elif the_object.name == 'N':
                    if move_is_valid(the_object, from_move, to_move):
                        if to_box in 'rnbkqp.':
                            update_board(from_move, to_move, the_object.name)
                            break
                    else:
                        print("invalid move, try again")

                elif the_object.name == 'B':
                    if move_is_valid(the_object, from_move, to_move):
                        if to_box in 'rnbkqp.':
                            update_board(from_move, to_move, the_object.name)
                            break
                    else:
                        print("invalid move, try again")

                elif the_object.name == 'Q':
                    if move_is_valid(the_object, from_move, to_move):
                        if to_box in 'rnbkqp.':
                            update_board(from_move, to_move, the_object.name)
                            break
                    else:
                        print("invalid move, try again")









        for i in range(4):
            move = input("Choose piece:  ")
            piece = get_object_name(move)
            move_piece(move)
            self.display_board(self.Board)
        ###















##############################
    def pawn_moves(move):
        yes = ['forward', 'forward_left_diagonal', 'forward_right_diagonal']
        if move in yes:
            return True
        return False

