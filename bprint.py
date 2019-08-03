
def print_solution(solution):
    """
    Outputs the solution according to the project specification
    """
    for i in range(1, len(solution)):
        print(get_move(solution[i-1], solution[i]))


def get_move(start_point, end_point):
    """
    returns the action taken to go from the start point to the end point as 
    a formatted string
    """
    
    EXIT_POSITION = [10, 10]

    result_str = ""
    for i in range(len(end_point)):
        
        # find the piece that has moved
        if end_point[i] != start_point[i]:

            # move action
            if abs(end_point[i][0] - start_point[i][0]) == 1 or abs(end_point[i][1] - start_point[i][1]) == 1:
                result_str += "MOVE from {} to {}.".format(tuple(start_point[i]), tuple(end_point[i]))

            # exit action
            elif end_point[i] == EXIT_POSITION :
                result_str += "EXIT from {}.".format(tuple(start_point[i]))

            # jump action
            else:
                result_str += "JUMP from {} to {}.".format(tuple(start_point[i]), tuple(end_point[i]))
            break
    return result_str
