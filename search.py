"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Asil Mian, John Stephenson
"""

import sys
import json

#game solutions as defined by project spec
GAME_SOLUTIONS = {"red": [[3,-3], [3,-2], [3,-1], [3,0]], "green": [[-3,3], [-2,3], [-1,3], [0,3]],
                 "blue":[[0,-3], [-1,-2], [-2,-1], [-3,0]]}


#currently set run debug_print
def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    board = Board(data)
    board.debug_print()
    
    print(board.create_board_struct())

class Board:
    #constructor class
    def __init__(self, starting_state):
        self.player_colour = starting_state["colour"]
        self.blocks = starting_state["blocks"]
        self.pieces = starting_state["pieces"]
        self.goals = GAME_SOLUTIONS[self.player_colour]
        

    #prints out the current game state
    #board state is no longer stored
    def debug_print(self):
        out_state = self.create_board()
        print_board(out_state, "debug_printing", True)

    #helper function for debug_print, creates the board
    #board is essentially a dictionary
    def create_board(self):
        out_board = {}
        for i in range(-3,4,1):
            for j in range(-3,4,1):
                out_board[(i,j)] = 0
        for piece in self.pieces:
            out_board[tuple(piece)] = self.player_colour
        for block in self.blocks:
            out_board[tuple(block)] = "blk"
        return out_board
    
    def create_board_struct(self):
        out_struct = {}
        for i in range(-3,4,1):
            for j in range(-3-(i<0)*i,4-(i>0)*i,1):
                pos = [i,j]
                out_struct[str(pos)] = self.findmoves(pos)
        

        return out_struct

    # def check_move(self, move):
    #     return (move in self.struct and 


    def findmoves(self, pos):

        #list of all moves in all direction
        moves = [[0, 1], [1, 0] , [1, -1], [0, -1], [-1, 0,], [-1, 1]]
        posmoves = []

        # create a list of all new positions given start pos
        for move in moves:
            posmoves.append(add(pos, move))
            
        # check and calcluate if any jumps need to take place
        
        jmp = []
        for tup in posmoves:
            if (tup in self.blocks or tup in self.pieces):
                jmp.append(add(tup,diff(tup,pos)))
            else:
                jmp.append(tup)

        # remove any moves that fall on a new block or outside the board

        sol = [tup for tup in jmp if (abs(tup[0])<=3 and abs(tup[1])<=3) and (tup not in self.blocks) and tup not in self.pieces]
        
        return sol


def add(a,b):
    return [x+y for x,y in zip(a,b)]

def diff(a,b):
    return [x-y for x,y in zip(a,b)]





def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.
    
    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using 
    the axial coordinate system outlined in the project specification) and the 
    values are formatted as strings and placed in the drawing at the corres- 
    ponding location (only the first 5 characters of each string are used, to 
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the 
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates 
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
