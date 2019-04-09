"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
John Stephenson (insert student id)
Asil Mian (867252)
"""

import sys
import json
from copy import deepcopy
import time
import operator
from math import sqrt
import heapq

#=================CONSTANTS======================================#

DEBUG = 0        #use to turn on debugging 
BOILER_PLATE_LENGTH = 45
BLOCK = "blk"

RED = "red"
GREEN = "green"
BLUE = "blue"

#exit position for each player
FINAL_ROWS = {RED : [[3,-3], [3, -2], [3, -1], [3, 0]],
                 GREEN: [[-3,3], [-2, 3], [-1, 3], [0, 3]],    
                 BLUE: [[-3,0], [-2, -1], [-1, -2], [0, -3]]}

GOAL_ROWS = {RED: [[4,-3], [4,-2], [4,-1]], 
                   GREEN: [[-3,4], [-2,4], [-1,4]] , 
                   BLUE: [[-3,-1], [-2,-2], [-1,-3]]}
                 
EXIT_POSITION = [10,10]   #to represent an offboard piece

#================================================================#


def main():
    start = time.time()
    with open(sys.argv[1]) as file:
        data = json.load(file)


    board = Board(data)
    if (DEBUG):
        board.debug_print()
    

    solution = a_star_search(board)

    if (DEBUG):
        animate(board,solution)


    print_solution(solution)
    print(time.time() - start)
    
#=======================Classes==================================#
class Board:
    """
    Class for representing a board.
    containes player information, and block information
    """

    def __init__(self, starting_state):
        self.player_colour = starting_state["colour"]
        self.blocks = starting_state["blocks"]
        self.pieces = starting_state["pieces"]
        self.printable_board = None    
        self.create_printable_board()
        self.final_row = FINAL_ROWS[self.player_colour]
        self.goal_row = GOAL_ROWS[self.player_colour]
        self.path_costs = None
        self.create_cost_dict()
        self.initial_state = State(self.pieces, None, self, 0)


    def debug_print(self):
        out_state = self.create_printable_board()
        print_board(out_state, "debug_printing", True)

    def create_printable_board(self):
        """
        helper function for debug_print
        creates the board as a dictionary
        """
        out_board = {}
        ran = range(-3, +3 + 1)

        for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
            out_board[qr] = ""

        for piece in self.pieces:
            out_board[tuple(piece)] = self.player_colour

        for block in self.blocks:
            out_board[tuple(block)] = BLOCK

        self.printable_board = out_board
        
        return out_board

    def create_cost_dict(self):
        # creates a dictionary of tiles on the board, and the number of jumps
        # required to reach the goal from that tile (in the absence of hops over friendly pieces)


        # initialise a dictionary with the exit position corresponding to a 0 distance
        cost_dict = {tuple(EXIT_POSITION): 0}

        queue = []

        
        # add the goal row to the dictionary
        for tile in self.goal_row:
            cost_dict[tuple(tile)] = 0
            queue.append(tuple(tile))

         # explore each currently reachable tile, and add it to the cost dictionary with a cost
         # of 1 greater than its parent
        while queue:
            current_tile = queue.pop(0)
            next_step = self.find_adjacent_tiles(current_tile)
            for step in next_step:
                
                if tuple(step) not in cost_dict:

                    cost_dict[tuple(step)] = cost_dict[current_tile] + 1
                    queue.append(tuple(step))

        
        
        self.path_costs = cost_dict
        return cost_dict


    def find_adjacent_tiles(self, tile):
        # method to find all adjecent tiles to a given tile

        moves = [[0, 1], [1, 0] , [1, -1], [0, -1], [-1, 0,], [-1, 1]]
        
        all_tiles = []
        for move in moves:
            
            new_tile = [a+b for a,b in zip(tile, move)]

            if new_tile in self.blocks and list(tile) not in self.goal_row:


                new_tile = [a+b for a,b in zip(new_tile, move)]
                

            all_tiles.append(new_tile)   
        


        return [x for x in all_tiles if tuple(x) in self.printable_board 
                                and x not in self.blocks]


class State:
    """
    Class represents a state
    i.e where each movable piece is and where it can possibly move
    """

    def __init__(self, poslist, parent_state, board, cost):
        self.poslist = poslist
        self.parent_state = parent_state
        self.obstacles = board.blocks + poslist
        self.board = board
        self.travel_cost = cost
        self.heuristic_cost = path_heuristic(self)

        self.total_cost = self.travel_cost + self.heuristic_cost
    
    def __str__(self):

        return "{}".format(self.poslist)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(tuple(tuple(x) for x in self.poslist))

    def __eq__(self, other):
        return self.poslist == other.poslist
    
    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def child_states(self):
        """
        finds the set of next possible states from the current state
        """
        move_actions = [[0, 1], [1, 0] , [1, -1], [0, -1], [-1, 0,], [-1, 1]]
        states = []
        
        #for each piece
        for i in range(len(self.poslist)):
            if self.poslist[i] not in EXIT_POSITION:

                #if the piece in question is in the final row, add make an exit action
                if self.poslist[i] in self.board.final_row:
                    temp = deepcopy(self.poslist)
                    temp[i] = EXIT_POSITION
                    states.append(State(temp, self, self.board, self.travel_cost + 1))

                #create all move actions
                for move in move_actions:
                    
                    temp = deepcopy(self.poslist)
                    
                    temp[i][0] = temp[i][0] + move[0] 
                    temp[i][1] = temp[i][1] + move[1] 
                    
                    #if any move action lands on obstacle, add jump action
                    if temp[i] in self.obstacles:
                    
                        temp[i][0] = temp[i][0] + move[0] 
                        temp[i][1] = temp[i][1] + move[1]
                    
                    #filter moves based on whether they land on the board or on obstacles
                    if tuple(temp[i]) in self.board.printable_board and temp[i] not in self.obstacles:

                        new_state = State(temp, self, self.board, self.travel_cost + 1)
                        if (new_state.heuristic_cost < self.heuristic_cost):
                            states.append(new_state)
        return states


    def is_goal(self):
        """
        returns true if all pieces are off the board
        """
        flag = True
        for pos in self.poslist:
            if pos != EXIT_POSITION:
                flag = False

        return flag

#================================================================#



#===============Search Functions=================================#


def a_star_search(board):
    """
    search the board for the solution and return the path 
    leading to the solution if one is found
    """
    start = board.initial_state
    #seen dictionary to prevent going to already seen states
    seen = {}
    queue = [start]
    heapq.heapify(queue)

    #while not all pieces are of the board
    while queue and not queue[0].is_goal():
        parent_state = heapq.heappop(queue)
        #check child states
        for child in parent_state.child_states():
            if child in seen:
                continue
            else:
                heapq.heappush(queue, child)
                seen[child] = True
        #parent_state.board.pieces = parent_state.poslist
        #parent_state.board.debug_print()

    #return if solution found
    if queue:
        return reconstruct_path(queue[0])

    else:
        return None


def euclidean_heuristic(state : State) -> float:
    """
    estimates the cost to end state from current state
    by using 3d cubic euclidian distance
    """
    
    h_n = 0
    colour = state.board.player_colour
    goals = GOAL_ROWS[colour]

    for piece_position in state.poslist:
        if piece_position == EXIT_POSITION:
            h_n -= 0

        #evaluate current state based on player colour
        else:
            cube_pos = cubify(piece_position)
            cube_goals = [cubify(x) for x in goals]

            if colour == RED:
                h_n += min(([(cube_pos[0]-x[0])**2 + (cube_pos[2]-x[2])**2 for x in cube_goals]))

            elif colour == GREEN:
                h_n += min(([(cube_pos[1]-x[1])**2 + (cube_pos[2]-x[2])**2 for x in cube_goals]))
        
            else:
                h_n += min(([(cube_pos[1]-x[1])**2 + (cube_pos[2]-x[2])**2 for x in cube_goals]))

    return h_n/10


def path_heuristic(state : State) -> float:

    h_n = 0
    
    for piece_position in state.poslist:
        
        h_n += state.board.path_costs[tuple(piece_position)]

    return h_n/2





def cubify(pos):
    """
    transform into 3d cubic co-ordinates
    """
    return [pos[0], pos[1], -pos[0]-pos[1]]  





def reconstruct_path(end_state):
    """
    track back the path to the initial state
    from the end_state
    """
    actions = []
    curr_state = end_state

    while curr_state.parent_state:
        actions.append(curr_state.poslist)
        curr_state = curr_state.parent_state
    actions.append(curr_state.poslist)

    #return action list in reverse order
    return actions[::-1]

#================================================================#


#================Printing Functions==============================#

def print_solution(solution):
    """
    Outputs the solution according to the project specification
    """
    print_boiler_plate()
    for i in range(1, len(solution)):
        print("{:11}".format(i) + " | " + print_move(solution[i-1], solution[i]))


def print_boiler_plate():
    """
    Boiler plate for standard out
    """
    print(" action no. | standard output")
    print("=" * BOILER_PLATE_LENGTH)

def print_move(start_point, end_point):
    """
    Prints the action taking a piece from start_point to
    end point
    """
    result_str = ""
    for i in range(len(end_point)):
        #find the piece that has moved
        if (end_point[i] != start_point[i]):

            #move action
            if abs(end_point[i][0] - start_point[i][0]) == 1 or \
                    abs(end_point[i][1] - start_point[i][1]) == 1:
                result_str += "MOVE from {} to {}.".format(tuple(start_point[i]), tuple(end_point[i]))

            #exit action
            elif end_point[i] == EXIT_POSITION :
                result_str += "EXIT from {}.".format(tuple(start_point[i]))

            #jump action
            else:
                result_str += "JUMP from {} to {}.".format(tuple(start_point[i]), tuple(end_point[i]))
            break
    return result_str

#================================================================#


def animate(board, solution):
    """
    displays an animation for the solution
    """
    for move in solution:
        board.pieces = move
        board.debug_print()
        time.sleep(1)


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
