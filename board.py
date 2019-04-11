

import heapq

from state import State
from bprint import print_board





class Board:
    
    
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
    
    MOVE_ACTIONS = [[0, 1], [1, 0] , [1, -1], [0, -1], [-1, 0,], [-1, 1]]
                     
    EXIT_POSITION = [10,10]   #to represent an offboard piece



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
        self.final_row = self.FINAL_ROWS[self.player_colour]
        self.goal_row = self.GOAL_ROWS[self.player_colour]
        self.path_costs = None
        self.shortest_path_costs()
        self.initial_state = State(self.pieces, None, self)

    # def debug_print(self):
    #     out_state = self.create_printable_board()
    #     print_board(out_state, "debug_printing", True)

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
            out_board[tuple(block)] = self.BLOCK

        self.printable_board = out_board
        return out_board

    def shortest_path_costs(self):
        """
        uses dijkstra's to find the shortest path from the any final row to all other positions
        and returns a dictionary with all the costs
        """
        #assume all final_row pieces can access exit postition
        cost_dict = {tuple(self.EXIT_POSITION): 0}
        entry_point = 0
        queue = []

        #add all final pieces to queue with cost 1
        for tile in self.final_row:
            if tile not in self.blocks:
                #a 3 point vector added to resolve same cost tiles sorting in heap
                queue.append([1, entry_point, tuple(tile)])
                cost_dict[tuple(tile)] = 1
                entry_point +=1
        heapq.heapify(queue)

        #while not visited tiles exist
        while queue:
            curr_tile = heapq.heappop(queue)
            #find cost for all adjacent tiles
            for adjacent_tile in self.find_adjacent_tiles(curr_tile[2]):

                #if adjacent tile not seen before
                if tuple(adjacent_tile) not in cost_dict:
                    cost_dict[tuple(adjacent_tile)] = curr_tile[0] + 1
                    heapq.heappush(queue, [curr_tile[0] + 1, entry_point, tuple(adjacent_tile)])
                    entry_point += 1

                #adjust if this path to adjacent tile is shorter
                elif cost_dict[tuple(adjacent_tile)] > curr_tile[0] + 1:
                    cost_dict[tuple(adjacent_tile)] = curr_tile[0] + 1
        self.path_costs = cost_dict



    def find_adjacent_tiles(self, tile):
        # method to find all adjecent tiles to a given tile
        
        all_tiles = []
        for move in self.MOVE_ACTIONS:
            new_tile = [a+b for a,b in zip(tile, move)]
            if new_tile not in self.blocks and tuple(new_tile) in self.printable_board:
                all_tiles.append(new_tile)
            elif new_tile in self.blocks:
                jump_tile = [a+b for a,b in zip(new_tile, move)]
                if jump_tile not in self.blocks and tuple(jump_tile) in self.printable_board:
                    all_tiles.append(jump_tile)

         
            all_tiles.append(new_tile)


        
        return [x for x in all_tiles if tuple(x) in self.printable_board 
                                and x not in self.blocks]