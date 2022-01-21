from pieces import *
from copy import deepcopy

class Board:
    """ Chess board class. """

# Initialize board
    def __init__(self):
        """ Board object constructor. """

        # Represent squares as 8x8 matrix. Rows are referred to as ranks
        # and columns are referred to as files per chess convention.
        self.board = [[None] * 8 for i in range(8)]

        # Map square designations in Terminal display to underlying indices.
        self.ranks = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
        self.files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        # Initialize a move-ledger.
        self.moves = []

        # Grant castling rights to both colors.
        self.white_can_castle = True
        self.black_can_castle = True

        # Initialize attributes for use in check, checkmate, stalemate,
        # and castling assessment.
        self.white_king = None
        self.white_rooks = []
        self.black_king = None
        self.black_rooks = []

        # Initialize lists of white and black pieces.
        self.white_pieces = []
        self.black_pieces = []

        # Initialize lists of pieces white and black have captures.
        self.white_captures = []
        self.black_captures = []

        # Initialize # moves white and black have made.
        self.num_white_moves = 0
        self.num_black_moves = 0

# Initialize piece
    def init_piece(self, piece, is_white):
        """ Initialize a piece on the chess board.
            NOTE: This method is only called when setting up the board for play. """

        # Place the piece in its square.    
        self.board[piece.rank][piece.file] = piece

        # Add it to white's pieces or black's pieces.
        if is_white:
            self.white_pieces += [piece]
        else:
            self.black_pieces += [piece]


# Vision
    def white_vision(self):
        """ Return the set of all squares white pieces attack and defend.
            NOTE: This does not include squares directly ahead of pawns. """

        vision = set()

        # Loop through all white pieces and add all squares in those pieces' vision lists.
        for piece in self.white_pieces:
            for square in piece.vision(self):
                vision.add((square[0], square[1]))

        return vision

    def black_vision(self):
        """ Return the set of all squares white pieces attack and defend.
            NOTE: This does not include squares directly ahead of pawns. """

        vision = set()

        # Loop through all black pieces and add all squares in those pieces' vision lists.
        for piece in self.black_pieces:
            for square in piece.vision(self):
                vision.add((square[0], square[1]))

        return vision


# Moves
    def white_moves(self):
        """ Return pieces and their corresponding lists of possible moves
            as key: value pairs in dictionary format. """

        moves = {}

        for white_piece in self.white_pieces:
            moves[white_piece] = white_piece.moves(self)

        return moves

    def black_moves(self):
        """ Return pieces and their corresponding lists of possible moves
            as key: value pairs in dictionary format. """

        moves = {}

        for black_piece in self.black_pieces:
            moves[black_piece] = black_piece.moves(self)

        return moves     


# In check
    def white_in_check(self):
        """ Return boolean value reflecting whether the white king is in check. """

        if (self.white_king.rank, self.white_king.file) in self.black_vision():
            return True

        else:
            return False

    def black_in_check(self):
        """ Return boolean value reflecting whether the black king is in check. """

        if (self.black_king.rank, self.black_king.file) in self.white_vision():
            return True

        else:
            return False


# Has move
    def white_has_move(self):
        """ Return boolean value reflecting whether white has a move. """

        # Create a deep copy of the board
        hypothetical = deepcopy(self)

        # Assign the white move dictionary to a variable
        piece_move_pairs = hypothetical.white_moves()

        # Loop through each white piece in the dictionary
        for white_piece in piece_move_pairs:

            # Assign that piece's moves to a variable
            piece_moves = piece_move_pairs[white_piece]

            # Loop through each of the piece's moves
            for move in piece_moves:

                # Execute the move on a hypothetical board
                hypothetical.move(move[0], move[1], move[2], move[3], move[4])

                # If as a result of the move the white king is not in check,
                # return True, i.e. white DOES have a move
                if (hypothetical.white_king.rank, hypothetical.white_king.file) not in hypothetical.black_vision():
                    return True

                # Reset the hypothetical board to a deep copy of the present board state
                hypothetical = deepcopy(self)

        # If the method reaches this line, no move out of check was found.
        return False

    def black_has_move(self):
        """ Return boolean value reflecting whether white has a move. """

        # See white_has_move() method annotations

        hypothetical = deepcopy(self)
        piece_move_pairs = hypothetical.black_moves()

        for black_piece in piece_move_pairs:
            piece_moves = piece_move_pairs[black_piece]

            for move in piece_moves:
                hypothetical.move(move[0], move[1], move[2], move[3], move[4])

                if (hypothetical.black_king.rank, hypothetical.black_king.file) not in hypothetical.white_vision():
                    return True

                hypothetical = deepcopy(self)


        return False


# Process move
    def process_white(self):
        """ 1. Determine whether white is checkmated or stalemated.
            2. If white has a move, obtain user input specifying
                the move the user would like to play and execute the move. """

        # Assign booleans reflecting whether white is in check and
        # whether white has a move out of check to variables
        in_check = self.white_in_check()
        has_move = self.white_has_move()

        # Black wins if white is in check and has no move out of check
        if in_check and not has_move:
            print('Checkmate. Black wins.')
            return False

        # Stalemate if white is not in check but can only move into check
        if not in_check and not has_move:
            print('Stalemate')
            return False

        # Notify player if in check but has a move
        # NOTE: method only reaches this line if has_move == True
        if in_check:
            print('Check.')

        # Initialize an empty list to contain all possible moves white has in the position
        possibles = []

        # Create a deep copy of the board
        hypothetical = deepcopy(self)

        # Use helper method to obtain dictionary of all white moves
        move_dict = hypothetical.white_moves()

        # Loop through each move each piece can make
        for piece in move_dict:
            for move in move_dict[piece]:

                # Execute the move on a hypothetical board
                hypothetical.move(move[0], move[1], move[2], move[3], move[4])

                # If the move does not expose the white king to check,
                # add it to 'possibles' in appropriate format for comparison
                # with user input
                if (hypothetical.white_king.rank, hypothetical.white_king.file) not in hypothetical.black_vision(): 
                    possibles += [[move[0], move[1], move[2], move[3]]]

                # Reset the hypothetical board
                hypothetical = deepcopy(self)

        # Initialize 'valid' as False and only set it to True
        # when the user has inputted a legal move
        valid = False

        # Initialize a variable to later store the move to be executed this turn
        move = None

        # While the user input does not specify a legal move...
        while not valid:

            # Ask the user for input
            user_input = input('Enter move: ')

            # Handle input in wrong format
            if len(user_input) != 5 \
                 or user_input[1] not in self.ranks \
                 or user_input[0] not in self.files \
                 or user_input[4] not in self.ranks \
                 or user_input[3] not in self.files \
                 or user_input[2] != ' ':
                print('Invalid format. Enter origin file/rank, destination file/rank, e.g. e2 e4')
                continue

            # Translate input from visual board notation to underlying board rank/file indices
            # using helper dictionaries
            init_rank = self.ranks[user_input[1]]
            init_file = self.files[user_input[0]]
            end_rank = self.ranks[user_input[4]]
            end_file = self.files[user_input[3]]

            # Handle input in proper format specifying impossible move
            if [init_rank, init_file, end_rank, end_file] not in possibles:
                print('Not a possible move. Try again.')
                continue

            # At this point in the method, the user has specified a possible move
            # Close the user input loop
            valid = True
        
        # White pawn promoting
        if self.board[init_rank][init_file].__class__.__name__ == 'WhitePawn':
            if init_rank == 1:

                # Offer player choice of knight, bishop, rook, and queen
                promotion_choice = ''

                # Insist choice is n, n, r, or q
                while promotion_choice not in ['n', 'b', 'r', 'q']:
                    promotion_choice = input('Choose n/b/r/q: ')

                # Format the move for execution according to user choice
                if promotion_choice == 'n':
                    move = [init_rank, init_file, end_rank, end_file, WhiteKnight(end_rank, end_file)]
                elif promotion_choice == 'b':
                    move = [init_rank, init_file, end_rank, end_file, WhiteBishop(end_rank, end_file)]
                elif promotion_choice == 'r':
                    move = [init_rank, init_file, end_rank, end_file, WhiteRook(end_rank, end_file)]
                elif promotion_choice == 'q':
                    move = [init_rank, init_file, end_rank, end_file, WhiteQueen(end_rank, end_file)]

                # Execute the move!
                self.move(move[0], move[1], move[2], move[3], move[4])

                # Return True signalling that a move was played
                return True

        # Non-promotion move
        # Format the move for execution according to user choice
        move = [init_rank, init_file, end_rank, end_file, None]

        # Execute the move!
        self.move(move[0], move[1], move[2], move[3], move[4])

        # Return True signalling that a move was played
        return True

    def process_black(self):
        """ 1. Determine whether black is checkmated or stalemated.
            2. If black has a move, obtain user input specifying
                the move the user would like to play and execute the move. """

        # See process_white() method annotations

        in_check = self.black_in_check()
        has_move = self.black_has_move()

        if in_check and not has_move:
            print('Checkmate. White wins.')
            return False

        if not in_check and not has_move:
            print('Stalemate')
            return False

        if in_check:
            print('Check.')

        possibles = []
        hypothetical = deepcopy(self)

        move_dict = hypothetical.black_moves()

        for piece in move_dict:
            for move in move_dict[piece]:

                hypothetical.move(move[0], move[1], move[2], move[3], move[4])

                if (hypothetical.black_king.rank, hypothetical.black_king.file) not in hypothetical.white_vision(): 
                    possibles += [[move[0], move[1], move[2], move[3]]]

                hypothetical = deepcopy(self)

        valid = False
        move = None

        while not valid:
            user_input = input('Enter move: ')

            if len(user_input) != 5:
                print('Invalid format. Enter origin file/rank, destination file/rank, e.g. e2 e4')
                continue

            init_rank = self.ranks[user_input[1]]
            init_file = self.files[user_input[0]]
            end_rank = self.ranks[user_input[4]]
            end_file = self.files[user_input[3]]

            if [init_rank, init_file, end_rank, end_file] not in possibles:
                print('Not a possible move. Try again.')
                continue

            valid = True
            
        # Black pawn promoting
        if self.board[init_rank][init_file].__class__.__name__ == 'BlackPawn':
            if init_rank == 6:
                promotion_choice = ''
                while promotion_choice not in ['n', 'b', 'r', 'q']:
                    promotion_choice = input('Choose n/b/r/q: ')

                if promotion_choice == 'n':
                    move = [init_rank, init_file, end_rank, end_file, BlackKnight(end_rank, end_file)]
                elif promotion_choice == 'b':
                    move = [init_rank, init_file, end_rank, end_file, BlackBishop(end_rank, end_file)]
                elif promotion_choice == 'r':
                    move = [init_rank, init_file, end_rank, end_file, BlackRook(end_rank, end_file)]
                elif promotion_choice == 'q':
                    move = [init_rank, init_file, end_rank, end_file, BlackQueen(end_rank, end_file)]

                self.move(move[0], move[1], move[2], move[3], move[4])
                return True

        # Non-promotion
        move = [init_rank, init_file, end_rank, end_file, None]
        self.move(move[0], move[1], move[2], move[3], move[4])

        return True


# Execute move on board
    def move(self, init_rank, init_file, end_rank, end_file, end_piece=None):
        """ Execute a chess move on a board object.
            Handle captures when they occur.
            Detect and properly execute special moves: promotion, en passant, castling.
            Update castling rights if appropriate.
            Update board object move ledger. 
            NOTE: end_piece defaults to None but takes the value of the promoted piece
                if promotion occurs. """
        
        # Assign the piece to be moved to a variable
        piece = self.board[init_rank][init_file]

        ### SPECIAL MOVES
        # 1. Promotion
        if end_piece:
            # print('Caught promotion')

            if piece.is_white:
                # Update white pieces: remove pawn, add promoted piece
                self.white_pieces.remove(piece)
                self.white_pieces += [end_piece]

                # Capture if appropriate
                if self.board[end_rank][end_file]:
                    self.white_captures += [self.board[end_rank][end_file]]
                    self.black_pieces.remove(self.board[end_rank][end_file])

                # Occupy square
                self.board[init_rank][init_file] = None
                self.board[end_rank][end_file] = end_piece

                return True

            else:
                # Update black pieces: remove pawn, add promoted piece
                self.black_pieces.remove(piece)
                self.black_pieces += [end_piece]

                # Capture if appropriate
                if self.board[end_rank][end_file]:
                    self.black_captures += [self.board[end_rank][end_file]]
                    self.white_pieces.remove(self.board[end_rank][end_file])

                # Occupy square
                self.board[init_rank][init_file] = None
                self.board[end_rank][end_file] = end_piece

                return True

        # 2. En passant
        # Moving piece is a pawn and it is capturing a pawn
        # of the opposite color on the square it moved THROUGH,
        # not the square it is ON
        if piece.__class__.__name__ in ['WhitePawn', 'BlackPawn']:
            if init_file != end_file and not self.board[end_rank][end_file]:
                # print('Caught en passant')

                # Update board appropriately
                if piece.__class__.__name__ == 'WhitePawn':
                    piece.rank = end_rank
                    piece.file = end_file
                    self.board[init_rank][init_file] = None
                    self.board[end_rank][end_file] = piece

                    self.white_captures += [self.board[end_rank + 1][end_file]]
                    self.black_pieces.remove(self.board[end_rank + 1][end_file])
                    self.board[end_rank + 1][end_file] = None

                    

                else:
                    piece.rank = end_rank
                    piece.file = end_file
                    self.board[init_rank][init_file] = None
                    self.board[end_rank][end_file] = piece

                    self.black_captures += [self.board[end_rank - 1][end_file]]
                    self.white_pieces.remove(self.board[end_rank - 1][end_file])
                    self.board[end_rank - 1][end_file] = None

                return True
        
        # 3. Castling
        # King and rook move simultaneously.
        if piece.__class__.__name__ in ['WhiteKing', 'BlackKing']:
            if abs(init_file - end_file) == 2:
                # print('Caught castling')

            # Update board appropriately.
                # White castle
                if piece.__class__.__name__ == 'WhiteKing':
                    # Kingside
                    if end_file == 6:
                        self.white_king.rank = 7
                        self.white_king.file = 6
                        self.board[init_rank][init_file] = None
                        self.board[7][6] = self.white_king

                        self.board[7][5] = self.board[7][7]
                        self.board[7][7] = None
                        self.board[7][5].rank, self.board[7][5].file = 7, 5

                    # Queenside
                    else:
                        self.white_king.rank = 7
                        self.white_king.file = 2
                        self.board[init_rank][init_file] = None
                        self.board[7][2] = self.white_king

                        self.board[7][3] = self.board[7][0]
                        self.board[7][0] = None
                        self.board[7][3].rank, self.board[7][3].file = 7, 3

                    self.white_can_castle = False       
                        
                # Black castle
                else:
                    # Kingside
                    if end_file == 6:
                        self.black_king.rank = 0
                        self.black_king.file = 6
                        self.board[init_rank][init_file] = None
                        self.board[0][6] = self.black_king

                        self.board[0][5] = self.board[0][7]
                        self.board[0][7] = None
                        self.board[0][5].rank, self.board[0][5].file = 0, 5

                    # Queenside
                    else:
                        self.black_king.rank = 0
                        self.black_king.file = 2
                        self.board[init_rank][init_file] = None
                        self.board[0][2] = self.black_king

                        self.board[0][3] = self.board[7][0]
                        self.board[0][0] = None
                        self.board[0][3].rank, self.board[0][3].file = 0, 3
                    
                    self.black_can_castle = False
    
                return True
        ### END SPECIAL MOVES

        # Handle capture if target square occupied
        if self.board[end_rank][end_file]:

            # White captures black
            if not self.board[end_rank][end_file].is_white:
                self.white_captures += [self.board[end_rank][end_file]]
                self.black_pieces.remove(self.board[end_rank][end_file])
            
            # Black captures white
            else:
                self.black_captures += [self.board[end_rank][end_file]]
                self.white_pieces.remove(self.board[end_rank][end_file])       

        # Update the moving piece's attributes
        if not end_piece:
            piece.rank = end_rank
            piece.file = end_file

        # Update the location of the piece on the board
        self.board[init_rank][init_file] = None
        self.board[end_rank][end_file] = piece

        # Check if rook or king moved and update castling rights accordingly
        if piece in self.white_rooks:
            self.white_rooks.remove(piece)
        if piece in self.black_rooks:
            self.black_rooks.remove(piece)
        if piece is self.white_king:
            self.white_can_castle = False
        if piece is self.black_king:
            self.black_can_castle = False

        # Add the move to the move ledger
        self.moves += [[piece, init_rank, init_file, end_rank, end_file, end_piece]]

        return True


# Print board
    def print_board(self):
        """ Print self.board in the Python terminal.
            Label ranks and files. Display pieces using
            unicode chess symbols. """

        print()
        print(' ' + '_' * 47 + ' ') 
        print('|     ' * 8 + '|')

        count = 0
        for rank in range(8):
            count += 1

            print('|', end='')

            for file in range(8):
                if self.board[rank][file]:
                    piece_string = str(self.board[rank][file])
                else:
                    piece_string = ' '
                print('  ' + piece_string + '  |', end='')

            if count == 1:
                print('  8', end='')
            elif count == 2:
                print('  7', end='')
            elif count == 3:
                print('  6', end='')
            elif count == 4:
                print('  5', end='')
            elif count == 5:
                print('  4', end='')
            elif count == 6:
                print('  3', end='')
            elif count == 7:
                print('  2', end='')
            elif count == 8:
                print('  1', end='')

            print()
            print(('|' + 5 * '_') * 8 + '|')

            if rank < 7:
                print('|     ' * 8 + '|')
        
        print()
        print('   ' + 'a' + '     ' + 'b' + '     ' + 'c' + '     ' + 'd' + '     ' + 'e' + '     ' + 'f' + '     ' + 'g' + '     ' + 'h')
        
        print()