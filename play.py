from board import *
from pieces import *

# Initialize board.
board = Board()

# Place white pawns on the board as white's pieces.
wp0 = WhitePawn(0)
wp1 = WhitePawn(1)
wp2 = WhitePawn(2)
wp3 = WhitePawn(3)
wp4 = WhitePawn(4)
wp5 = WhitePawn(5)
wp6 = WhitePawn(6)
wp7 = WhitePawn(7)
board.init_piece(wp0, True)
board.init_piece(wp1, True)
board.init_piece(wp2, True)
board.init_piece(wp3, True)
board.init_piece(wp4, True)
board.init_piece(wp5, True)
board.init_piece(wp6, True)
board.init_piece(wp7, True)

# Place black pawns on the board as black's pieces.
bp0 = BlackPawn(0)
bp1 = BlackPawn(1)
bp2 = BlackPawn(2)
bp3 = BlackPawn(3)
bp4 = BlackPawn(4)
bp5 = BlackPawn(5)
bp6 = BlackPawn(6)
bp7 = BlackPawn(7)
board.init_piece(bp0, False)
board.init_piece(bp1, False)
board.init_piece(bp2, False)
board.init_piece(bp3, False)
board.init_piece(bp4, False)
board.init_piece(bp5, False)
board.init_piece(bp6, False)
board.init_piece(bp7, False)

# Place white knights on board as white's.
wn1 = WhiteKnight(7, 1)
wn2 = WhiteKnight(7, 6)
board.init_piece(wn1, True)
board.init_piece(wn2, True)

# Place black knights as black's.
bn1 = BlackKnight(0, 1)
bn2 = BlackKnight(0, 6)
board.init_piece(bn1, False)
board.init_piece(bn2, False)

# Place white bishops as white's.
wb1 = WhiteBishop(7, 2)
wb2 = WhiteBishop(7, 5)
board.init_piece(wb1, True)
board.init_piece(wb2, True)

# Place black bishops as black's.
bb1 = BlackBishop(0, 2)
bb2 = BlackBishop(0, 5)
board.init_piece(bb1, False)
board.init_piece(bb2, False)

# Place white rooks as white's.
wr1 = WhiteRook(7, 0)
wr2 = WhiteRook(7, 7)
board.init_piece(wr1, True)
board.init_piece(wr2, True)
board.white_rooks += [wr1, wr2]

# Place black rooks as black's.
br1 = BlackRook(0, 0)
br2 = BlackRook(0, 7)
board.init_piece(br1, False)
board.init_piece(br2, False)
board.black_rooks += [br1, br2]

# Place white queen as white's.
wq = WhiteQueen(7, 3)
board.init_piece(wq, True)

# Place black queen as black's.
bq = BlackQueen(0, 3)
board.init_piece(bq, False)

# Place white king as white's.
wk = WhiteKing(7, 4)
board.init_piece(wk, True)
board.white_king = wk

# Place black king as black's.
bk = BlackKing(0, 4)
board.init_piece(bk, False)
board.black_king = bk

print('----------------------------------------')
print('Welcome to Python chess in the terminal.')
print()
print('Enter moves as initial square/end square pairs, e.g. e2 e4')

# Loop until checkmate or stalemate, in which case
# process_color() will return False and the program will end.
while True:

    board.print_board()
    if not board.process_white():
        break

    board.print_board()
    if not board.process_black():
        break

