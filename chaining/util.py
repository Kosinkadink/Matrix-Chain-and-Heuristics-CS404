import random
import copy
import os

# get location of main directory
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__)))  # directory from which this script is ran
main_dir = os.path.realpath(os.path.join(__location__,'..'))


def read_config(filename):
	c_dict = {}
	with open(os.path.join(main_dir,filename),"rb") as conf:
		for line in conf:
			try:
				key,val = line.strip().split('=')
				key = key.strip()
				val = val.strip()
				c_dict[key] = val
			except Exception,e:
				pass
	return c_dict



class ExperimentResult(object):
	def __init__(self,name="NO_NAME"):
		self.name = name
		self.heuristics = {}
		self.heuristic_normal = {}

	def __getitem__(self,key):
		return self.getAverage(key)

	def __setitem__(self,key,item):
		self.heuristics.setdefault(key,[]).append(item)

	def getAverage(self,key):
		if len(self.heuristics[key]) == 0:
			return None
		else:
			return sum(self.heuristics[key])/len(self.heuristics[key])

	def getName(self):
		return self.name

	def printData(self):
		print self.name
		print '{}:{}'.format('OPT',self.getAverage('OPT'))
		print '{}:{}'.format('A',self.getAverage('A'))
		print '{}:{}'.format('B',self.getAverage('B'))
		print '{}:{}'.format('C',self.getAverage('C'))
		print '{}:{}'.format('D',self.getAverage('D'))
		print '{}:{}'.format('E',self.getAverage('E'))
		print '{}:{}'.format('F',self.getAverage('F'))

	def printNormal(self):
		print self.name
		print '{}:{}'.format('OPT',self.heuristic_normal['OPT'])
		print '{}:{}'.format('A',self.heuristic_normal['A'])
		print '{}:{}'.format('B',self.heuristic_normal['B'])
		print '{}:{}'.format('C',self.heuristic_normal['C'])
		print '{}:{}'.format('D',self.heuristic_normal['D'])
		print '{}:{}'.format('E',self.heuristic_normal['E'])
		print '{}:{}'.format('F',self.heuristic_normal['F'])

	def printSpecificData(self,key,func):
		print '{}:{}'.format(key,func(key))

	def getNormalAverage(self,key):
		return float(sum(self.heuristic_normal[key]))/len(self.heuristic_normal[key])

	def getNormalMin(self,key):
		return min(self.heuristic_normal[key])

	def getNormalMax(self,key):
		return max(self.heuristic_normal[key])

	def printNormalResults(self):
		print self.name
		names = ['OPT','A','B','C','D','E','F']
		for name in names:
			self.printSpecificData(name,self.getNormalMin)
			self.printSpecificData(name,self.getNormalAverage)
			self.printSpecificData(name,self.getNormalMax)



	def performCalcAndClear(self):
		for key,value in self.heuristics.iteritems():
			if key == 'OPT':
				self.heuristic_normal.setdefault(key,[]).append(1.0)
			else:
				self.heuristic_normal.setdefault(key,[]).append(float(sum(self.heuristics[key]))/sum(self.heuristics['OPT']))
		self.heuristics = {}



class MatrixChain(object):

	def __init__(self,chain_length=0,low=7,high=17):
		self.LOW_VAL = low
		self.HIGH_VAL = high
		if chain_length <= 0:
			self.chain = None
		else:
			self.chain = self.generateRandomChain(chain_length)
		self.default_chain = copy.copy(self.chain)

	def __len__(self):
		return len(self.chain)

	def __getitem__(self, key):
		return self.chain[key]

	def resetChain(self):
		self.chain = copy.copy(self.default_chain)

	def setChain(self,new_chain):
		self.chain = copy.copy(new_chain)
		self.default_chain = copy.copy(self.chain)

	# return chain list
	def getChain(self):
		return self.chain

	# generate chain of side lengths wi
	def generateRandomChain(self,n_matrices):
		new_chain = []
		for i in range(0,n_matrices+1):
			new_chain.append(random.randint(self.LOW_VAL,self.HIGH_VAL))
		return new_chain

	# choose a 
	def getRandomOperator(self):
		return random.randint(1,len(self.chain)-2)

	# return cost for chosen operator pair, update list
	def performOperation(self,index):
		cost = self.getOperationCost(index)
		self.chain.pop(index)
		return cost

	def getOperationCost(self,index):
		cost = self.chain[index-1]*self.chain[index]*self.chain[index+1]
		return cost
