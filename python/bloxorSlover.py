

def findPath(startPos, endPos):
	queue = []
	prevLUT = {}
	i, a, k, p, np

	#Build tree
	queue.append(endPos)
	prevLUT[endPos.MakeKey()] = None
	while(len(queue)):
		p = queue.pop(0)
		a = FileterPositions()
		for i in range(len(a)):
			np = a[i]
			k = np.MakeKey()
			if prevLUT[k] != "undefined":
				continue

			queue.append(np)
			prevLUT[k] = p

			if np.EqualP(startPos) == True:
				queue = []
				break

	#walk tree backwards
	rv = []
	
