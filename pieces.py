from board import *

class Piece:
    """ Parent class for chess pieces. """

    def __init__(self):
        """ Object instance constructor. """

        # All pieces get rank, file, and captured attributes.
        self.rank = None
        self.file = None

# Pawns
class Pawn(Piece):
    """ Pawn parent class. """

    def __init__(self):
        """ Pawn constructor. """

        super().__init__()

        # Pawns worth 1 point
        self.value = 1

class WhitePawn(Pawn):
    """ White pawn class. """

    def __init__(self, file):
        """ White pawn constructor. """

        super().__init__()

        # White pawns start on rank with index six.
        self.rank = 6

        # White pawns initiated with a file index as argument.
        self.file = file

        # White pawns are white.
        self.is_white = True

    def __repr__(self):
        """ Return unicode pawn character. """

        return '♟︎'

    def vision(self, board):
        """ Return squares white pawn attacks or defends. """

        vision = []

        # Diagonal left
        if 0 <= self.rank - 1 and 0 <= self.file - 1:
            vision += [[self.rank - 1, self.file - 1]]

        # Diagonal right
        if 0 <= self.rank - 1 and self.file + 1 <= 7:
            vision += [[self.rank - 1, self.file + 1]]

        return vision

    def moves(self, board):
        """ Return each of the moves a pawn can make. 
            Format: [piece, current rank, current file, resulting piece, new rank, new file]. """

        moves = []
        vision = self.vision(board)

        # Diagonal captures (possibility of promotion)
        for square in vision:
            if board.board[square[0]][square[1]] != None:
                if not board.board[square[0]][square[1]].is_white:
                    # Capture: promotion
                    if self.rank - 1 == 0:
                        for choice in [WhiteKnight, WhiteBishop, WhiteRook, WhiteQueen]:
                            promoted_piece = choice(square[0], square[1])
                            moves += [[self.rank, self.file, square[0], square[1], promoted_piece]]
                    # Capture: regular
                    else:
                        moves += [[self.rank, self.file, square[0], square[1], None]]

        # Two-square starting move
        if self.rank == 6 and board.board[4][self.file] == None and board.board[5][self.file] == None:
            moves += [[self.rank, self.file, self.rank - 2, self.file, None]]

        # One-square advance (possibility of promotion)
        if board.board[self.rank - 1][self.file] == None:

            # Advance: promotion
            if self.rank - 1 == 0:
                for choice in [WhiteKnight, WhiteBishop, WhiteRook, WhiteQueen]:
                    promoted_piece = choice(square[0], square[1])
                    moves += [[self.rank, self.file, self.rank - 1, self.file, promoted_piece]]

            # Advance: regular
            else:
                moves += [[self.rank, self.file, self.rank - 1, self.file, None]]

        # En passant
        # Check that white pawn is on correct rank for en passant capture
        if self.rank == 3:
            # Check that a black pawn moved previously
            if board.moves[-1][0].__class__.__name__ == 'BlackPawn':
                # Check that the black pawn advanced two squares
                if abs(board.moves[-1][1] - board.moves[-1][3]) == 2:
                    # Check that the square the black pawn moved through is in this pawn's vision
                    if [board.moves[-1][3] - 1, board.moves[-1][4]] in self.vision(board):
                        moves += [[self.rank, self.file, board.moves[-1][3] - 1, board.moves[-1][4], None]]


        return moves

class BlackPawn(Pawn):
    """ Black pawn class. """

    def __init__(self, file):
        """ Black pawn constructor. """
        
        super().__init__()
        self.rank = 1
        self.file = file
        self.is_white = False

    def __repr__(self):
        """ Return unicode pawn character. """

        return '♙'

    def vision(self, board):
        """ Return squares black pawn attacks or defends. """

        vision = []

        # Diagonal left
        if self.rank + 1 <= 7 and 0 <= self.file - 1:
            vision += [[self.rank + 1, self.file - 1]]

        # Diagonal right
        if self.rank + 1 <= 7 and self.file + 1 <= 7:
            vision += [[self.rank + 1, self.file + 1]]

        return vision

    def moves(self, board):
        """ Return each of the moves a pawn can make. 
            Format: [piece, current rank, current file, resulting piece, new rank, new file]. """

        moves = []
        vision = self.vision(board)

        # Diagonal captures (possibility of promotion)
        for square in vision:
            if board.board[square[0]][square[1]] != None:
                if board.board[square[0]][square[1]].is_white:
                    # Capture: promotion
                    if self.rank + 1 == 7:
                        for choice in [BlackKnight, BlackBishop, BlackRook, BlackQueen]:
                            promoted_piece = choice(square[0], square[1])
                            moves += [[self.rank, self.file, square[0], square[1], promoted_piece]]
                    # Capture: regular
                    else:
                        moves += [[self.rank, self.file, square[0], square[1], None]]

        # Two-square starting move
        if self.rank == 1 and board.board[3][self.file] == None and board.board[2][self.file] == None:
            moves += [[self.rank, self.file, self.rank + 2, self.file, None]]

        # One-square advance (possibility of promotion)
        if board.board[self.rank + 1][self.file] == None:

            # Advance: promotion
            if self.rank + 1 == 7:
                for choice in [BlackKnight, BlackBishop, BlackRook, BlackQueen]:
                    promoted_piece = choice(square[0], square[1])
                    moves += [[self.rank, self.file, self.rank + 1, self.file, promoted_piece]]

            # Advance: regular
            else:
                moves += [[self.rank, self.file, self.rank + 1, self.file, None]]

        # En passant
        # Check that white pawn is on correct rank for en passant capture
        if self.rank == 4:
            # Check that a black pawn moved previously
            if board.moves[-1][0].__class__.__name__ == 'WhitePawn':
                # Check that the black pawn advanced two squares
                if abs(board.moves[-1][3] - board.moves[-1][1]) == 2:
                    # Check that the square the black pawn moved through is in this pawn's vision
                    if [board.moves[-1][3] + 1, board.moves[-1][4]] in self.vision(board):
                        moves += [[self.rank, self.file, board.moves[-1][3] + 1, board.moves[-1][4], None]]

        return moves

# Knights
class Knight(Piece):
    """ Knight parent class. """

    def __init__(self, rank, file):
        """ Knight constructor. """

        super().__init__()
        self.rank = rank
        self.file = file

        # Knights worth 3
        self.value = 3

    def vision(self, board):
        """ Return squares knight attacks/defends.
            Knights jump in Ls. """

        vision = []

        # Check all squares a knight's L away from its present square
        if 0 <= self.rank - 2 <= 7 and 0 <= self.file - 1 <= 7:
            vision += [[self.rank - 2, self.file - 1]]

        if 0 <= self.rank + 2 <= 7 and 0 <= self.file - 1 <= 7:
            vision += [[self.rank + 2, self.file - 1]]

        if 0 <= self.rank - 2 <= 7 and 0 <= self.file + 1 <= 7:
            vision += [[self.rank - 2, self.file + 1]]

        if 0 <= self.rank + 2 <= 7 and 0 <= self.file + 1 <= 7:
            vision += [[self.rank + 2, self.file + 1]]

        if 0 <= self.rank - 1 <= 7 and 0 <= self.file - 2 <= 7:
            vision += [[self.rank - 1, self.file - 2]]

        if 0 <= self.rank - 1 <= 7 and 0 <= self.file + 2 <= 7:
            vision += [[self.rank - 1, self.file + 2]]

        if 0 <= self.rank + 1 <= 7 and 0 <= self.file + 2 <= 7:
            vision += [[self.rank + 1, self.file + 2]]

        if 0 <= self.rank + 1 <= 7 and 0 <= self.file - 2 <= 7:
            vision += [[self.rank + 1, self.file - 2]]

        return vision

    def moves(self, board):
        """ Return a list of moves a knight can make. """

        moves = []

        # Loop through all squares in the knight's vision and add any squares
        # that are unoccupied or occupied by pieces of the opposite color
        for square in self.vision(board):
            if not board.board[square[0]][square[1]]:
                moves += [[self.rank, self.file, square[0], square[1], None]]
            else:
                if board.board[square[0]][square[1]].is_white != self.is_white:
                    moves += [[self.rank, self.file, square[0], square[1], None]]

        return moves

class WhiteKnight(Knight):
    """ White knight class. """

    def __init__(self, rank, file):
        """ White knight constructor. """

        super().__init__(rank, file)
        self.is_white = True

    def __repr__(self):
        """ Return unicode knight character. """

        return '♞'

class BlackKnight(Knight):
    """ Black knight class. """

    def __init__(self, rank, file):
        """ Black knight constructor. """

        super().__init__(rank, file)
        self.is_white = False

    def __repr__(self):
        """ Return unicode knight character. """

        return '♘'

# Bishops
class Bishop(Piece):
    """ Bishop parent class. """

    def __init__(self, rank, file):
        """ Bishop constructor. """

        super().__init__()
        self.rank = rank
        self.file = file

        # Bishops worth 3
        self.value = 3

    def vision(self, board):
        """ Return squares bishop attacks/defends.
            Bishops move along diagonals. """

        vision = []

        # Store current rank and file in variables.
        current_rank, current_file = self.rank, self.file

        # Check for open down-right squares.
        # Add open squares to moves.
        while current_rank + 1 <= 7 and current_file + 1 <= 7:
            if not board.board[current_rank + 1][current_file + 1]:
                vision += [[current_rank + 1, current_file + 1]]
                current_rank += 1
                current_file += 1
            else:
                break

        # No more open squares. If the next square along this diagonal
        # is occupied by a piece, add it to vision.
        if current_rank + 1 <= 7 and current_file + 1 <= 7:
            vision += [[current_rank + 1, current_file + 1]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open up-right squares.
        # Add open squares to moves.
        while current_rank - 1 >= 0 and current_file + 1 <= 7:
            if not board.board[current_rank - 1][current_file + 1]:
                vision += [[current_rank - 1, current_file + 1]]
                current_rank -= 1
                current_file += 1
            else:
                break

        # No more open squares. If the next square along this diagonal
        # is occupied by a piece of the opposite color, add it to moves.
        if current_rank - 1 >= 0 and current_file + 1 <= 7:
            vision += [[current_rank - 1, current_file + 1]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open up-left squares.
        # Add open squares to moves.
        while current_rank - 1 >= 0 and current_file - 1 >= 0:
            if not board.board[current_rank - 1][current_file - 1]:
                vision += [[current_rank - 1, current_file - 1]]
                current_rank -= 1
                current_file -= 1
            else:
                break

        # No more open squares. If the next square along this diagonal
        # is occupied by a piece of the opposite color, add it to moves.
        if current_rank - 1 >= 0 and current_file - 1 >= 0:
            vision += [[current_rank - 1, current_file - 1]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open down-right squares.
        # Add open squares to moves.
        while current_rank + 1 <= 7 and current_file - 1 >= 0:
            if not board.board[current_rank + 1][current_file - 1]:
                vision += [[current_rank + 1, current_file - 1]]
                current_rank += 1
                current_file -= 1
            else:
                break

        # No more open squares. If the next square along this diagonal
        # is occupied by a piece of the opposite color, add it to moves.
        if current_rank + 1 <= 7 and current_file - 1 >= 0:
            vision += [[current_rank + 1, current_file - 1]]

        return vision

    def moves(self, board):
        """ Return a list of moves a bishop can make. """

        moves = []

        # Loop through all squares in bishop's vision and add any squares
        # that are unoccupied or occupied by pieces of the opposite color
        for square in self.vision(board):
            if not board.board[square[0]][square[1]]:
                moves += [[self.rank, self.file, square[0], square[1], None]]
            else:
                if board.board[square[0]][square[1]].is_white != self.is_white:
                    moves += [[self.rank, self.file, square[0], square[1], None]]

        return moves

class WhiteBishop(Bishop):
    """ White bishop class. """

    def __init__(self, rank, file):
        """ White bishop constructor. """

        super().__init__(rank, file)
        self.is_white = True

    def __repr__(self):
        """ Return unicode bishop character. """

        return '♝'

class BlackBishop(Bishop):
    """ Black bishop class. """

    def __init__(self, rank, file):
        """ Black bishop constructor. """

        super().__init__(rank, file)
        self.is_white = False

    def __repr__(self):
        """ Return unicode bishop character. """

        return '♗'

# Rooks
class Rook(Piece):
    """ Rook parent class. """

    def __init__(self, rank, file):
        """ Rook constructor. """

        super().__init__()
        self.rank = rank
        self.file = file

        # Rooks worth 5
        self.value = 5

    def vision(self, board):
        """ Return a list of squares a rook attacks/defends. 
            Rooks move vertically and horizontally. """

        vision = []

        # Store current rank and file in variables.
        current_rank, current_file = self.rank, self.file

        # Check for open squares below.
        # Add open squares to moves.
        while current_rank + 1 <= 7:
            if not board.board[current_rank + 1][current_file]:
                vision += [[current_rank + 1, current_file]]
                current_rank += 1
            else:
                break

        # No more open squares. If the next square down is
        # occupied by a piece of the opposite color, add it to moves.
        if current_rank + 1 <= 7:
            vision += [[current_rank + 1, current_file]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open squares above.
        # Add open squares to moves.
        while current_rank - 1 >= 0:
            if not board.board[current_rank - 1][current_file]:
                vision += [[current_rank - 1, current_file]]
                current_rank -= 1

            else:
                break

        # No more open squares. If the next square up is
        # occupied by a piece of the opposite color, add it to moves.
        if current_rank - 1 >= 0:
            vision += [[current_rank - 1, current_file]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open squares to the right.
        # Add open squares to moves.
        while current_file + 1 <= 7:
            if not board.board[current_rank][current_file + 1]:
                vision += [[current_rank, current_file + 1]]
                current_file += 1
            else:
                break

        # No more open squares. If the next square down is
        # occupied by a piece of the opposite color, add it to moves.
        if current_file + 1 <= 7:
            vision += [[current_rank, current_file + 1]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open squares to the left.
        # Add open squares to moves.
        while current_file - 1 >= 0:
            if not board.board[current_rank][current_file - 1]:
                vision += [[current_rank, current_file - 1]]
                current_file -= 1
            else:
                break

        # No more open squares. If the next square down is
        # occupied by a piece of the opposite color, add it to moves.
        if current_file - 1 >= 0:
                vision += [[current_rank, current_file - 1]]

        return vision

    def moves(self, board):
        """ Return a list of moves a rook can make. """

        moves = []

        # Loop through all squares in rook's vision and add any squares
        # that are unoccupied or occupied by pieces of the opposite color        
        for square in self.vision(board):
            if not board.board[square[0]][square[1]]:
                moves += [[self.rank, self.file, square[0], square[1], None]]
            else:
                if board.board[square[0]][square[1]].is_white != self.is_white:
                    moves += [[self.rank, self.file, square[0], square[1], None]]

        return moves

class WhiteRook(Rook):
    """ White Rook class. """

    def __init__(self, rank, file):
        """ White rook constructor. """

        super().__init__(rank, file)
        self.is_white = True

    def __repr__(self):
        """ Return unicode rook character. """

        return '♜'

class BlackRook(Rook):
    """ Black Rook class. """

    def __init__(self, rank, file):
        """ Black rook constructor. """

        super().__init__(rank, file)
        self.is_white = False

    def __repr__(self):
        """ Return unicode rook character. """

        return '♖'

# Queens
class Queen(Piece):
    """ Queen parent class. """

    def __init__(self, rank, file):
        """ Queen constructor. """

        super().__init__()
        self.rank = rank
        self.file = file

        # Queens worth 9
        self.value = 9

    def vision(self, board):
        """ Return squares a queen attacks/defends.
            A queen moves diagonally, vertically, and horizontally. """

        vision = []

        #
        #
        # BEGIN ROOK BEHAVIOR

        # Store current rank and file in variables.
        current_rank, current_file = self.rank, self.file

        # Check for open squares below.
        # Add open squares to moves.
        while current_rank + 1 <= 7:
            if not board.board[current_rank + 1][current_file]:
                vision += [[current_rank + 1, current_file]]
                current_rank += 1
            else:
                break

        # No more open squares. If the next square down is
        # occupied by a piece of the opposite color, add it to moves.
        if current_rank + 1 <= 7:
            vision += [[current_rank + 1, current_file]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open squares above.
        # Add open squares to moves.
        while current_rank - 1 >= 0:
            if not board.board[current_rank - 1][current_file]:
                vision += [[current_rank - 1, current_file]]
                current_rank -= 1

            else:
                break

        # No more open squares. If the next square up is
        # occupied by a piece of the opposite color, add it to moves.
        if current_rank - 1 >= 0:
            vision += [[current_rank - 1, current_file]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open squares to the right.
        # Add open squares to moves.
        while current_file + 1 <= 7:
            if not board.board[current_rank][current_file + 1]:
                vision += [[current_rank, current_file + 1]]
                current_file += 1
            else:
                break

        # No more open squares. If the next square down is
        # occupied by a piece of the opposite color, add it to moves.
        if current_file + 1 <= 7:
            vision += [[current_rank, current_file + 1]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open squares to the left.
        # Add open squares to moves.
        while current_file - 1 >= 0:
            if not board.board[current_rank][current_file - 1]:
                vision += [[current_rank, current_file - 1]]
                current_file -= 1
            else:
                break

        # No more open squares. If the next square down is
        # occupied by a piece of the opposite color, add it to moves.
        if current_file - 1 >= 0:
                vision += [[current_rank, current_file - 1]]       

        # END ROOK BEHAVIOR
        # 
        #     

        #
        #
        # BEGIN BISHOP BEHAVIOR

        # Store current rank and file in variables.
        current_rank, current_file = self.rank, self.file

        # Check for open down-right squares.
        # Add open squares to moves.
        while current_rank + 1 <= 7 and current_file + 1 <= 7:
            if not board.board[current_rank + 1][current_file + 1]:
                vision += [[current_rank + 1, current_file + 1]]
                current_rank += 1
                current_file += 1
            else:
                break

        # No more open squares. If the next square along this diagonal
        # is occupied by a piece , add it to vision.
        if current_rank + 1 <= 7 and current_file + 1 <= 7:
            vision += [[current_rank + 1, current_file + 1]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open up-right squares.
        # Add open squares to moves.
        while current_rank - 1 >= 0 and current_file + 1 <= 7:
            if not board.board[current_rank - 1][current_file + 1]:
                vision += [[current_rank - 1, current_file + 1]]
                current_rank -= 1
                current_file += 1
            else:
                break

        # No more open squares. If the next square along this diagonal
        # is occupied by a piece of the opposite color, add it to moves.
        if current_rank - 1 >= 0 and current_file + 1 <= 7:
            vision += [[current_rank - 1, current_file + 1]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open up-left squares.
        # Add open squares to moves.
        while current_rank - 1 >= 0 and current_file - 1 >= 0:
            if not board.board[current_rank - 1][current_file - 1]:
                vision += [[current_rank - 1, current_file - 1]]
                current_rank -= 1
                current_file -= 1
            else:
                break

        # No more open squares. If the next square along this diagonal
        # is occupied by a piece of the opposite color, add it to moves.
        if current_rank - 1 >= 0 and current_file - 1 >= 0:
            vision += [[current_rank - 1, current_file - 1]]

        # Reset current square.
        current_rank, current_file = self.rank, self.file

        # Check for open down-right squares.
        # Add open squares to moves.
        while current_rank + 1 <= 7 and current_file - 1 >= 0:
            if not board.board[current_rank + 1][current_file - 1]:
                vision += [[current_rank + 1, current_file - 1]]
                current_rank += 1
                current_file -= 1
            else:
                break

        # No more open squares. If the next square along this diagonal
        # is occupied by a piece of the opposite color, add it to moves.
        if current_rank + 1 <= 7 and current_file - 1 >= 0:
            vision += [[current_rank + 1, current_file - 1]]       
        
        # END BISHOP BEHAVIOR
        # 
        # 

        return vision

    def moves(self, board):
        """ Return a list of move a queen can make. """

        moves = []

        # Loop through all squares in queen's vision and add any squares
        # that are unoccupied or occupied by pieces of the opposite color
        for square in self.vision(board):
            if not board.board[square[0]][square[1]]:
                moves += [[self.rank, self.file, square[0], square[1], None]]
            else:
                if board.board[square[0]][square[1]].is_white != self.is_white:
                    moves += [[self.rank, self.file, square[0], square[1], None]]

        return moves

class WhiteQueen(Queen):
    """ White queen class. """

    def __init__(self, rank, file):
        """ White queen constructor. """

        super().__init__(rank, file)
        self.is_white = True

    def __repr__(self):
        """ Return unicode queen character. """

        return '♛'

class BlackQueen(Queen):
    """ Black queen class. """

    def __init__(self, rank, file):
        """ Black queen constructor. """

        super().__init__(rank, file)
        self.is_white = False

    def __repr__(self):
        """ Return unicode queen character. """

        return '♕'

# Kings
class King(Piece):
    """ King parent class. """

    def __init__(self, rank, file):
        """ King constructor. """

        super().__init__()
        self.rank = rank
        self.file = file

        # A king has an attribute whose value reflects whether the king is in check
        self.in_check = False

    def vision(self, board):
        """ Return a list of squares a king attacks/defends.
            Kings can see all adjacent squares, including
            diagonal adjacencies. """

        vision = []

        current_rank, current_file = self.rank, self.file

        # Squares below
        if current_rank < 7:
            vision += [[current_rank + 1, current_file]]

            if current_file > 0:
                vision += [[current_rank + 1, current_file - 1]]
            if current_file < 7:
                vision += [[current_rank + 1, current_file + 1]]

        # Squares above
        if current_rank > 0:
            vision += [[current_rank - 1, current_file]]

            if current_file > 0:
                vision += [[current_rank - 1, current_file - 1]]
            if current_file < 7:
                vision += [[current_rank - 1, current_file + 1]]

        # Square to right
        if current_file < 7:
            vision += [[current_rank, current_file + 1]]
        
        # Square to left
        if current_file > 0:
            vision += [[current_rank, current_file - 1]]

        return vision

class WhiteKing(King):
    """ White king class. """

    def __init__(self, rank, file):
        """ White king constructor. """

        super().__init__(rank, file)
        self.is_white = True

    def __repr__(self):
        """ Return unicode king character. """

        return '♚'

    def moves(self, board):
        """ Return a list of moves a white king can make. """

        moves = []

        # Loop through all squares in king's vision and add any squares
        # that are unoccupied or occupied by pieces of the opposite color        
        for square in self.vision(board):
            if not board.board[square[0]][square[1]]:
                moves += [[self.rank, self.file, square[0], square[1], None]]
            else:
                if board.board[square[0]][square[1]].is_white != self.is_white:
                    moves += [[self.rank, self.file, square[0], square[1], None]]

        # Check for castling rights
        if board.white_can_castle:

            # Kingside castle
            # Check for rook on kingside corner
            if board.board[7][7]:

                # Check that the rook has castling rights
                if board.board[7][7] in board.white_rooks:

                    # Check that the squares in between the king and rook are empty
                    if not board.board[7][5] and not board.board[7][6]:

                        # Check that the king is not castling from, through, or into check
                        if (7, 4) not in board.black_vision() and (7, 5) not in board.black_vision() and (7,6) not in board.black_vision():
                            
                            # Conditions for kingside castling have been met;
                            # include kingside castling in move list
                            moves += [[self.rank, self.file, 7, 6, None]]

            # Queenside castle
            # Same logic, mirror image
            if board.board[7][0]:
                if board.board[7][0] in board.white_rooks:
                    if not board.board[7][1] and not board.board[7][2] and not board.board[7][3]:
                        if (7, 2) not in board.black_vision() and (7, 3) not in board.black_vision() and (7,4) not in board.black_vision():
                            moves += [[self.rank, self.file, 7, 2, None]]

        return moves

class BlackKing(King):
    """ Black king class. """

    def __init__(self, rank, file):
        """ Black king constructor. """

        super().__init__(rank, file)
        self.is_white = False

    def __repr__(self):
        """ Return unicode king character. """

        return '♔'

    def moves(self, board):
        """ Return a list of moves a black king can make. """

        # See WhiteKing moves() method annotations

        moves = []

        for square in self.vision(board):
            if not board.board[square[0]][square[1]]:
                moves += [[self.rank, self.file, square[0], square[1], None]]
            else:
                if board.board[square[0]][square[1]].is_white != self.is_white:
                    moves += [[self.rank, self.file, square[0], square[1], None]]

        # Check for castling
        if board.black_can_castle:
            # print('Castling rights identified')

            # Kingside castle
            if board.board[0][7]:
                if board.board[0][7] in board.black_rooks:
                    if not board.board[0][5] and not board.board[0][6]:
                        if (0, 4) not in board.white_vision() and (0, 5) not in board.white_vision() and (0,6) not in board.white_vision():
                            moves += [[self.rank, self.file, 0, 6, None]]

            # Queenside
            if board.board[0][0]:
                if board.board[0][0] in board.black_rooks:
                    if not board.board[0][1] and not board.board[0][2] and not board.board[0][3]:
                        if (0, 2) not in board.white_vision() and (0, 3) not in board.white_vision() and (0,4) not in board.white_vision():
                            moves += [[self.rank, self.file, 0, 2, None]]

        return moves