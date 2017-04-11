import os

from chaining.util import MatrixChain,read_config
from chaining.strategies import performHeuristics,performHeuristicsMANUAL


__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__)))  # directory from which this script is ran


#exampleChain = [7,8,9,10,11]
#exampleChain = [5,7,3,2,8]

#matChain = MatrixChain()
#matChain.setChain(exampleChain)

#matChain = MatrixChain(5)

def main():
	conf = read_config('conf.txt')
	# check if want to read from file
	if conf['FILE_TO_READ']:
		with open(os.path.join(__location__,conf['FILE_TO_READ']),'rb') as dimfile:
			conf['DIM_LIST'] = dimfile.readline()
	if conf['DIM_LIST']:
		conf['DIM_LIST'] = [int(dim.strip()) for dim in conf['DIM_LIST'].split(',')]
		results = performHeuristicsMANUAL(conf)
	else:
		results = performHeuristics(conf)
	for result in results:
		result.printNormalResults()

if __name__ == '__main__':
	main()
