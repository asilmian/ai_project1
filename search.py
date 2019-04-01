"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Asil Mian, John Stephenson
"""

import sys
import json
import copy
import time

#game solutions as defined by project spec

GAME_SOLUTIONS = {"red": [(3,-3), (3,-2), (3,-1), (3,0)], "green": [(-3,3), (-2,3), (-1,3), (0,3)], "blue":[(0,-3), (-1,-2), (-2,-1), (-3,0)]}

OFF_BOARD = {
    "red": ((4,-2),),
    "green": ((-2, 4),),
    "blue": ((-2,-2),)
}



#currently set run debug_print
def main():
    
    


    with open(sys.argv[1]) as file:
        data = json.load(file)
    board = Board(data)
    board.debug_print()
    

    # print(shortest_path_bfs(board, board.pieces, GAME_SOLUTIONS[board.player_colour]))

    solution = bfs_paths_new(board, board.pieces, GAME_SOLUTIONS[board.player_colour])

    
    animate(board, solution)

    print(solution)



class Board:
    #constructor class
    def __init__(self, starting_state):
        self.player_colour = starting_state["colour"]
        self.blocks = starting_state["blocks"]
        self.pieces = starting_state["pieces"]
        self.goals = GAME_SOLUTIONS[self.player_colour]
        self.exit = OFF_BOARD[self.player_colour]
        self.board = None
        
        self.create_board()

    #prints out the current game state
    #board state is no longer stored
    def debug_print(self):
        out_state = self.create_board()
        print_board(out_state, "debug_printing", True)

    #helper function for debug_print, creates the board
    #board is essentially a dictionary
    def create_board(self):
        out_board = {}

        ran = range(-3, +3 + 1)

        for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
            out_board[qr] = ""

        for piece in self.pieces:
            out_board[tuple(piece)] = self.player_colour

        for block in self.blocks:
            out_board[tuple(block)] = "blk"

        self.board = out_board
        
        return out_board

    # def create_board_struct(self):
    #     out_struct = {}
    #     for i in range(-3,4,1):
    #         for j in range(-3-(i<0)*i,4-(i>0)*i,1):
    #             pos = [i,j]
    #             out_struct[tuple(pos)] = set(self.findmoves(pos))
                
    #     self.graph = out_struct

    # def check_move(self, move):
    #     return (move in self.struct and 


def findmoves(board, poslist):
    
    #list of all moves in all direction
    moves = [[0, 1], [1, 0] , [1, -1], [0, -1], [-1, 0,], [-1, 1]]
    posmoves = []
    

    # create a list of all new positions given start pos
    for i in range(len(poslist)):
        
        if poslist[i] not in board.exit:

            for move in moves:
                
                temp = [list(x) for x in poslist]
                
                temp[i][0] = temp[i][0]+move[0]
                temp[i][1] = temp[i][1]+move[1]
                
                if (temp[i] in board.blocks or temp[i] in [list(x) for x in poslist]):
                    temp[i][0] = temp[i][0]+move[0]
                    temp[i][1] = temp[i][1]+move[1]

                tempf = [tuple(l) for l in temp]

                posmoves.append(tuple(tempf))
    
  

    
    # check and calcluate if any jumps need to take place

    # remove any moves that fall on a new block or outside the board

    sol = [movelist for movelist in posmoves if isvalidmove(board, movelist)]
    
    for i in range(len(poslist)):
        templist = list(poslist)
        if templist[i] in board.goals:
            templist[i] = board.exit[0]
            sol.append(tuple(templist))

    
    return tuple(sol)

# Adapted from https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
# ---------------------------------------------------------------


def reconstruct_path(prev_dict, end_state):
    path = []
    state = end_state
    while prev_dict[state] is not None:
        path.append(state)
        state=prev_dict[state]
    return path[::-1]


def bfs_paths_new(board, start, goal):
    
    vert_prev = {tuple(tuple(x) for x in start): None}
    queue = [tuple(tuple(x) for x in start)]
    
    while queue and not check_win(queue[-1], board):
        vertex = queue.pop(0)

        for move in findmoves(board, vertex):
            # if move in vert_prev:
            #     continue
            queue.append(move)
            vert_prev[move] = vertex
    
    if queue:
        goal = queue[-1]
        path = reconstruct_path(vert_prev, goal)
        return path
    else:
        print("No path found...")





def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        
        vertex = queue.pop(0)
        
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited

def bfs_paths(board, start, goal):
    
    
    start = tuple(tuple(x) for x in start)
    
    queue = [(start, [start])]
    

    while queue:
        
        vertex, path = queue.pop(0)
        
        
        for next in set(findmoves(board, vertex)) - set(path):
           
            if check_win(next,board):
                yield path + [next]
            else:
                
                queue.append((next, path + [next]))

def shortest_path_bfs(board, start, goal):
    try:
        return next(bfs_paths(board, start, goal))
    except StopIteration:
        return None

# -------------------------------------------------------------------


def dfs_paths(board, start, goal):
    
    
    start = tuple(tuple(x) for x in start)
    
    stack = [(start, [start])]
    

    while stack:
        
        (vertex, path) = stack.pop(-1)
        
        
        for next in set(findmoves(board, vertex)) - set(path):
           
            if check_win(next,board):
                yield path + [next]
            else:
                
                stack.append((next, path + [next]))


def shortest_path_dfs(board, start, goal):
    try:
        return next(dfs_paths(board, start, goal))
    except StopIteration:
        return None


def dls_paths(board, start, goal, depth):

    start = tuple(tuple(x) for x in start)
    
    stack = [(start, [start]), 0]
    

    while stack and (len(stack[-1][1]) <= depth):
        
        (vertex, path) = stack.pop(-1)
        
        
        for next in set(tuple(findmoves(board, vertex))) - set(path):
           
            if check_win(next,board):
                yield path + [next]
            else:
                
                stack.append((next, path + [next]))
    

def shortest_path_dls(board, start, goal, depth):
    try:
        return next(dls_paths(board, start, goal, depth))
    except StopIteration:
        return None








def animate(board, solution):
    

    for move in solution:
        board.pieces = move
        board.debug_print()
        time.sleep(1)




def can_exit(move, goal):
    for m in move:
        if m not in goal:
            # print("left from {0}".format(m))
            return False
    return True


def check_win(move, board):
    for m in move:
        if m not in board.exit:
            return False
    return True



def add(a,b):
    return [x+y for x,y in zip(a,b)]

def diff(a,b):
    return [x-y for x,y in zip(a,b)]

def cubeify(hexpos):
    return (hexpos[0], hexpos[1], -hexpos[0]-hexpos[1])

def hexify(cubepos):
    return (cubepos[0], cubepos[1])

def isvalidmove(board, move):

    flag = True
    for tup in move:
        
        
        if((len(move) != len(set(move)) or (tup not in board.board) or (list(tup) in board.blocks))):
            flag = False
          
    return flag


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
