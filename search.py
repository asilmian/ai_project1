"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
John Stephenson (587636)
Asil Mian (867252)
"""

import sys
import json
import time
import heapq
from board import Board
from state import State
from bprint import print_solution
#=================CONSTANTS======================================#

DEBUG = 1        #use to turn on debugging 

#================================================================#

def main():
    start = time.time()
    with open(sys.argv[1]) as file:
        data = json.load(file)

    board = Board(data)

    solution = a_star_search(board)

    print_solution(solution)
    print(time.time() - start)



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
            heapq.heappush(queue, child)
            seen[child] = True
        #parent_state.board.pieces = parent_state.poslist
        #parent_state.board.debug_print()
    #return if solution found
    if queue:
        return reconstruct_path(queue[0])

    else:
        return None


def path_heuristic(state : State) -> float:
    h_n = 0
    
    for piece_position in state.poslist:
        
        h_n += state.board.path_costs[tuple(piece_position)]

    return h_n/2


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

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
