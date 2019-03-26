def findmoves(pos):

	moves = [[0, 1], [1, 0] , [1, -1]]
	posmoves = []

	for move in moves:
		posmoves.append([a + b for a, b in zip(move, pos)])
		posmoves.append([a + b for a, b in zip([-x for x in move], pos)])

	sol = [tup for tup in posmoves if (abs(tup[0])<=3 and abs(tup[1])<=3) ]
	return sol


print(findmoves([0,0]))

