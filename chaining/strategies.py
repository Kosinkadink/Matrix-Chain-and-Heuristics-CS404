from util import MatrixChain,ExperimentResult


def performHeuristics():
	global_low = 7
	global_high = 17
	# set stuff
	lengths_to_test = [10,15,20,25]
	lengths_results = []
	reps_to_do = 30

	# get all strats in order
	all_strats = get_all_strategies()


	# set current iteration
	for curr_length in lengths_to_test:
		# create a result for this length and name it
		results = ExperimentResult(str(curr_length))
		for rep in range(reps_to_do):
			# create matrix chain to perform test
			matrixChain = MatrixChain(curr_length)
			for strat in all_strats:
				results[strat[1]] = strat[0](matrixChain)
			results.performCalcAndClear()
		# add this result
		lengths_results.append(results)
				
	return lengths_results


# returns list containing all strat functions
def get_all_strategies():
	all_strats = []
	all_strats.append((optimal,'OPT'))
	all_strats.append((strategyA,'A'))
	all_strats.append((strategyB,'B'))
	all_strats.append((strategyC,'C'))
	all_strats.append((strategyD,'D'))
	all_strats.append((strategyE,'E'))
	all_strats.append((strategyF,'F'))
	return all_strats

# returns optimal cost
def optimal(matrixChain):
	total_cost = 0
	# create a 2d matrix to do the things
	table = [[[(0,0),0] for x in range(len(matrixChain)-1)] for y in range(len(matrixChain)-1)]
	# initialize table
	for c in range(0,len(matrixChain)-1):
		table[c][c][0] = (matrixChain[c],matrixChain[c+1])

	# fill in, going from bottom of each column  
	for x in range(1,len(matrixChain)-1):
		for y in range(x-1,-1,-1):
			all_costs = []
			temp_x = y
			temp_y = y+1
			while temp_x < x:
				curr_cost = 0
				# add stored costs
				curr_cost += table[temp_x][y][1]
				curr_cost += table[x][temp_y][1]
				# add cost of current multiplication
				dim1 = table[temp_x][y][0][0]
				dim2 = table[temp_x][y][0][1]
				dim3 = table[x][temp_y][0][1]
				curr_cost += dim1*dim2*dim3
				all_costs.append([(dim1,dim3),curr_cost])
				# increment temp x and temp y
				temp_x += 1
				temp_y += 1
			# get minimum cost + dims from options
			table[x][y] = min(all_costs, key=lambda c: c[1])

	#for row in table:
	#	print row

	# get cost from top right corner of table
	total_cost = table[len(matrixChain)-2][0][1]

	matrixChain.resetChain()
	return total_cost

# performs strategy a: remove largest dimension first
def strategyA(matrixChain):
	total_cost = 0
	while len(matrixChain) > 2:
		max_operator = 1
		max_length = 0
		for op in range(1,len(matrixChain)-1):
			curr_length = matrixChain[op]
			if curr_length > max_length:
				max_operator = op
				max_length = curr_length
		# perform max operator
		total_cost += matrixChain.performOperation(max_operator)
	matrixChain.resetChain()
	return total_cost

# performs strategy b: perform most expensive operation first
def strategyB(matrixChain):
	total_cost = 0
	while len(matrixChain) > 2:
		max_operator = 1
		max_cost = matrixChain[max_operator]
		for op in range(1,len(matrixChain)-1):
			curr_cost = matrixChain.getOperationCost(op)
			if curr_cost > max_cost:
				max_operator = op
				max_cost = curr_cost
		# perform max operator
		total_cost += matrixChain.performOperation(max_operator)
	matrixChain.resetChain()
	return total_cost

# performs strategy c: remove smallest dimension first
def strategyC(matrixChain):
	total_cost = 0
	while len(matrixChain) > 2:
		min_operator = 1
		min_length = matrixChain[min_operator]
		for op in range(1,len(matrixChain)-1):
			curr_length = matrixChain[op]
			if curr_length < min_length:
				min_operator = op
				min_length = curr_length
		# perform max operator
		total_cost += matrixChain.performOperation(min_operator)
	matrixChain.resetChain()
	return total_cost

# performs strategy d: perform least expensive operation first
def strategyD(matrixChain):
	total_cost = 0
	while len(matrixChain) > 2:
		min_operator = 1
		min_cost = matrixChain.getOperationCost(min_operator)
		for op in range(1,len(matrixChain)-1):
			curr_cost = matrixChain.getOperationCost(op)
			if curr_cost < min_cost:
				min_operator = op
				min_cost = curr_cost
		# perform max operator
		total_cost += matrixChain.performOperation(min_operator)
	matrixChain.resetChain()
	return total_cost

# performs strategy e: choose random operations
def strategyE(matrixChain):
	total_cost = 0
	all_costs = []
	while len(all_costs) < (len(matrixChain)-1)*2:
		curr_cost = 0
		while len(matrixChain) > 2:
			curr_cost += matrixChain.performOperation(matrixChain.getRandomOperator())
		all_costs.append(curr_cost)
		matrixChain.resetChain()
	
	total_cost = min(all_costs)
	matrixChain.resetChain()
	return total_cost

# performs strategy f: go in order 
def strategyF(matrixChain):
	total_cost = 0
	while len(matrixChain) > 2:
		total_cost += matrixChain.performOperation(1)
	matrixChain.resetChain()
	return total_cost
