def findmoves(pos):

	moves = [[0, 1], [1, 0] , [1, -1]]
	posmoves = []

	for move in moves:
		posmoves.append([a + b for a, b in zip(move, pos)])
		posmoves.append([a + b for a, b in zip([-x for x in move], pos)])

	sol = [tup for tup in posmoves if (abs(tup[0])<=3 and abs(tup[1])<=3) ]
	return sol




a = [(1,2), (2,3)]



for i in range(len(a)):
	if a[i] == (1,2):
		a[i] = (0,0)




print(a)





    	



