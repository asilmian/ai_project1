


class Board:
    #constructor class
    def __init__(self, starting_state):
        self.player_colour = starting_state["colour"]
        self.blocks = starting_state["blocks"]
        self.pieces = starting_state["pieces"]
        
        self.initial_state = State(self.pieces, None, self)


        self.printable_board = None    
        self.create_printable_board()

        self.goal = None
        self.final_row = None
        self.fetch_goal_info()


    
    def fetch_goal_info(self):
        self.goal = [10,10]

        if self.player_colour == 'red':
            self.final_row = [[3,-3], [3, -2], [3, -1], [3, 0]]
        
        if self.player_colour == 'green':
            self.final_row = [[-3,3], [-2, 3], [-1, 3], [0, 3]]

        if self.player_colour == 'blue':
            self.final_row = [[-3,0], [-2, -1], [-1, -2], [0, -3]]



    def debug_print(self):
        out_state = self.create_printable_board()
        self.print_board(out_state, "debug_printing", True)

    #helper function for debug_print, creates the board
    #board is essentially a dictionary
    def create_printable_board(self):
        out_board = {}

        ran = range(-3, +3 + 1)

        for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
            out_board[qr] = ""

        for piece in self.pieces:
            out_board[tuple(piece)] = self.player_colour

        for block in self.blocks:
            out_board[tuple(block)] = "blk"

        self.printable_board = out_board
        
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


class State:
    

    def __init__(self, poslist, parent, board):
        self.poslist = poslist
        self.parent = parent
        self.obstacles = board.blocks + poslist
        
        self.board = board
    
    # def children(self):
    #     moves = [[0, 1], [1, 0] , [1, -1], [0, -1], [-1, 0,], [-1, 1]]
    #     posmoves = []

    #     for move in posmoves:



if __name__ == "__main__":
    print("Youre executing boardutil")