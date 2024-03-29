
class State:
    """
    Represents a state of the board.
    State is defined by the position of each player piece on the board
    and is unique up to the ordering of the pieces
    """

    EXIT_POSITION = [10, 10]
    MOVE_ACTIONS = [[0, 1], [1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1]]

    def __init__(self, poslist, parent_state, board=None):
        self.poslist = poslist
        self.parent_state = parent_state

        #contruct by parent state
        if parent_state:
            self.board = parent_state.board
            self.travel_cost = parent_state.travel_cost + 1
            self.obstacles = self.board.blocks + self.poslist

        #construct by board
        elif board:
            self.board = board
            self.travel_cost = 0
            self.obstacles = board.blocks + poslist
        
        self.heuristic_cost = self.path_heuristic()
        self.total_cost = self.travel_cost + self.heuristic_cost
    

    def __str__(self):
        return "{}".format(self.poslist)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        #hash ignoring the ordering of the positions in poslist
        return hash(tuple(tuple(x) for x in sorted(self.poslist)))
    
    def __eq__(self, other):
        #ignoring ordering while testing for equality
        return set([tuple(x) for x in self.poslist]) == set([tuple(x) for x in other.poslist])
    
    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def child_states(self):
        """
        finds the set of next possible states from the current state
        """
        states = []
        
        # for each piece
        for i in range(len(self.poslist)):
            if self.poslist[i] not in self.EXIT_POSITION:

                # if the piece in question is in the final row, add make an exit action
                if self.poslist[i] in self.board.final_row:
                    temp_poslist = self.poslist.copy()
                    temp_poslist[i] = self.EXIT_POSITION
                    states.append(State(temp_poslist, self))
                    continue
                # create the move action
                for move in self.MOVE_ACTIONS:
                    temp_move = [self.poslist[i][0] + move[0], self.poslist[i][1] + move[1]] 
                    
                    # if the move action lands on obstacle, turn into jump action
                    if temp_move in self.obstacles:
                        temp_move[0] += move[0] 
                        temp_move[1] += move[1]
                    
                    # filter moves based on whether they land on the board or on obstacles
                    if tuple(temp_move) in self.board.printable_board and temp_move not in self.obstacles:
                        temp = self.poslist.copy()
                        temp[i] = temp_move
                        new_state = State(temp, self)
                        
                        states.append(new_state)
        return states

    def is_goal(self):
        """
        returns true if all pieces are off the board
        """
        flag = True
        for pos in self.poslist:
            if pos != self.EXIT_POSITION:
                flag = False

        return flag

    def path_heuristic(self):
        """
        finds the minimum number of jump actions needed to get to the nearest goal state
        """

        h_n = 0 
        for piece_position in self.poslist:
        
            h_n += self.board.path_costs[tuple(piece_position)]

        return h_n/2