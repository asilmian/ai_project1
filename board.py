import heapq
from state import State


class Board:
    """
    represents the board.
    contains player information, block information
    and dictionary with shortest path cost to each postition from goal state
    """


#================== Constants ================================== #
    BLOCK = "blk"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    
    # exit position for each player
    FINAL_ROWS = {RED: [[3, -3], [3, -2], [3, -1], [3, 0]],
                  GREEN: [[-3, 3], [-2, 3], [-1, 3], [0, 3]],
                  BLUE: [[-3, 0], [-2, -1], [-1, -2], [0, -3]]}

    MOVE_ACTIONS = [[0, 1], [1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1]]
                     
    EXIT_POSITION = [10, 10]   # to represent an off-board piece

# =============================================================== #

    def __init__(self, starting_state):

        self.player_colour = starting_state["colour"]
        self.blocks = starting_state["blocks"]
        self.pieces = starting_state["pieces"]
        self.final_row = self.FINAL_ROWS[self.player_colour]

        self.printable_board = self.create_printable_board()

        self.path_costs = self.shortest_path_costs()

        self.initial_state = State(self.pieces, None, self)

    def create_printable_board(self):
        """
        creates the map of the board
        add each legal position of the board into a dictionary
        """
        out_board = {}
        ran = range(-3, +3 + 1)

        for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
            out_board[qr] = ""

        
        for piece in self.pieces:
            out_board[tuple(piece)] = self.player_colour

        for block in self.blocks:
            out_board[tuple(block)] = self.BLOCK

        return out_board

    def shortest_path_costs(self):
        """
        uses dijkstra's to find the shortest path from the any final row to all other positions
        and returns a dictionary with all the costs
        """
        # assume all final_row pieces can access exit position
        cost_dict = {tuple(self.EXIT_POSITION): 0}
        entry_point = 0
        queue = []

        # add all final pieces to queue with cost 1
        for tile in self.final_row:
            if tile not in self.blocks:

                # a 3 point vector added to resolve same cost position sorting in heap
                queue.append([1, entry_point, tuple(tile)])
                cost_dict[tuple(tile)] = 1
                entry_point += 1
        heapq.heapify(queue)

        # while not visited tiles exist
        while queue:
            curr_tile = heapq.heappop(queue)

            #find cost for all adjacent tiles
            for adjacent_tile in self.find_adjacent_tiles(curr_tile[2]):

                # if adjacent tile not seen before
                if tuple(adjacent_tile) not in cost_dict:
                    cost_dict[tuple(adjacent_tile)] = curr_tile[0] + 1
                    heapq.heappush(queue, [curr_tile[0] + 1, entry_point, tuple(adjacent_tile)])
                    entry_point += 1

                # adjust if this path to adjacent tile is shorter
                elif cost_dict[tuple(adjacent_tile)] > curr_tile[0] + 1:
                    cost_dict[tuple(adjacent_tile)] = curr_tile[0] + 1

        return cost_dict

    def find_adjacent_tiles(self, tile):
        """
        Returns all the possible moves from current tile
        only considers jumps over blocks and not pieces
        """
        
        all_tiles = []

        for move in self.MOVE_ACTIONS:
            new_tile = [a+b for a, b in zip(tile, move)]
            
            #jump over blocks if possible
            if new_tile in self.blocks:
                new_tile = [a+b for a, b in zip(new_tile, move)]
            all_tiles.append(new_tile)

        return [x for x in all_tiles if tuple(x) in self.printable_board and x not in self.blocks]
