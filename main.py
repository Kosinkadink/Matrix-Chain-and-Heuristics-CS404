import os

from chaining.util import MatrixChain
from chaining.strategies import performHeuristics

#exampleChain = [7,8,9,10,11]
#exampleChain = [5,7,3,2,8]

#matChain = MatrixChain()
#matChain.setChain(exampleChain)

#matChain = MatrixChain(5)

def main():
	results = performHeuristics()
	for result in results:
		result.printNormalResults()

if __name__ == '__main__':
	main()
