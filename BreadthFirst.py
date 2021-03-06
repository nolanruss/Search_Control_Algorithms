'''

BreadthFirst search is a program that finds optimal solutions to games
(using the Game class) by iterating through all possible moves and
comparing to both the game goal state and all previous states visited.


'''
import Game
from EightPuzzle import EightPuzzle
from MissionaryCannibal import MissionaryCannibal
from SlidingTiles import SlidingTiles


class BreadthFirst:	

	def __init__(self, game):
		self.game = game
		self.goals = set()
		print('bfs created')


	'''
		buildGraph generates states and stores them in the graph{} 
		dictionary until either the goal is reached, or a set number
		of moves are performed.
	'''
	def buildGraph(self):
		MAX_MOVES = 10 # The max number of iterations before restarting.
		goalFound = False
		while not goalFound: # Generate nodes until goal is reached.
			start = self.game.gen_start()
			for gameGoal in self.game.goals:
				self.goals.add(gameGoal) 
			graph = {} # Stores visited states as (Parent, kids) pairs.

			# Get the initial move information for dictionary.
			parent, children = self.game.gen_moves(start)
			print('Parent: ', parent, ' Child: ',children)
			graph.update({parent: set(children)})
			print(graph)

			# For each key in the graph, add children to the dictionary
			# and check if a goal state is reached
			maxMoveCounter = 0
			# The game restarts if no goal is found in MAX_MOVES
			while maxMoveCounter < MAX_MOVES: 
				# Iterate through all keys and generate a dictionary
				# of new move states.
				tempGraph, goalFound = self.searchKeys(graph)
				# Update graph with the new moves stored in tempGraph.
				graph.update(tempGraph)
				print('updating dictionary')
				print('Size of dictionary', len(graph))
				
				maxMoveCounter += 1
		print('Verify all keys found: ')
		for key in graph:
			for vertex in graph[key]:
				if vertex not in graph:
					print('Key ', vertex, ' not found')	
				else:
					print('Key ', vertex, ' found')
		print('goalFound: ', goalFound)
		return self.game, graph	


	'''
		searchKeys searches through all child states for each parent
		key.  Child states not present as keys in the dictionary are
		added as new keys.  If a goal state has not yet been reached,
		child states are generated for the new keys.  Otherwise they
		are capped as and empty set().

	'''
	def searchKeys(self, searchGraph):

		goalFound = False
		graphKeys = searchGraph.keys()
		tempDict = {}
		# Iterate through every key in the graph. 
		for key in graphKeys:
			# Check that each path is present as a graph key.
			for vertex in searchGraph[key]:
				# If child state is not in graph, add it.
				if vertex not in searchGraph:
					# If the goal isn't reached, add new states.
					if not goalFound:
						# Generate child states and add to the dictionary.
						movestart, newstates = self.game.gen_moves(vertex)
						tempDict.update({movestart: set(newstates)})
						print('Tempdict size: ', len(tempDict))
					# If the goal was reached previously.
					else: 
						# Set all child states as an empty set
						print('vertex capped as set(): ', vertex)
						tempDict.update({vertex: set()})
				# Compare the present vertex to the goal state.
				elif vertex in self.goals:
				#	print('goal found!')
					goalFound = True
		print('Start state: ', self.game.start)
		return tempDict, goalFound


	'''
		bfs first calls buildGraph to generate a dictionary that
		has reached the goal state. The method then searches each state
		in the graph to find the shortest path to the goal. 

	'''
	def bfs(self):	
		# Generate a game and graph containing the goal state.
		legalGame, legalGraph = self.buildGraph()
		goalState = tuple(legalGame.goals)
		startState = legalGame.start
		# Store the states not yet visited in queue.
		queue = [(tuple(startState), [tuple(startState)])]
		# While the queue is not empty, perform the search.
		qcnt = 0
		while queue:
			qcnt += 1
			(vertex, path) = queue.pop(0) # Pop the current graph key.
			# For each child of a vertex/key compare to the states seen.
			# The subtraction leaves only unvisited paths in each key.
			cnt = 0
#			print('Iteration: ', qcnt, ' Printing key:')
			for next in legalGraph[vertex] - set(path):
				cnt += 1
#				print(cnt, ' Next: ', next, '\n   Goal: ', goalState, ' equal?', next == goalState)
				# If already visited state, skip to next child state.
				if next in goalState:
#					print('Goal found, path+[next]:\n', path+[next])
					yield path + [next]
				else:
					queue.append((next, path + [next]))	
#					print('appending', next)


	'''
		shortestPath calls bfs (AKA the breadth first search function)
		and is meant to return all successful paths.
	'''
	def shortestPath(self):
		try:
			return next(self.bfs())
		except StopIteration:
			return None


'''
	All games and output format are run below.
'''

f = open("SearchResults.txt", 'a')
eightGame = EightPuzzle()
bfsearch = BreadthFirst(eightGame)
eightSolutions = (bfsearch.shortestPath())
strSolutions = str(eightSolutions)
f.write(('Path to success: ' + str(strSolutions)))
for i in eightSolutions:
	f.write(('\n' + str(i) + '\n'))
for state in eightSolutions:
        f.write(str(('\nMove#\n', state[0:3], '\n', state[3:6], '\n', state[6:9])))

missionGame = MissionaryCannibal()
bfSearchMission = BreadthFirst(missionGame)
missionSolutions = (bfSearchMission.shortestPath())
f.write(('\nMissionary Path to success: ' + str(missionSolutions)))
#for i in range(len(missionSolutions)):
#        f.write(('\nMove#',i, missionSolutions[i], ':\n', missionSolutions[i][0:3], '\n', missionSolutions[i][3:6], '\n', missionSolutions[i][6:9]))

tileGame = SlidingTiles()
bfSearchTiles = BreadthFirst(tileGame)
tileSolutions = (bfSearchTiles.shortestPath())
f.write(('\nSliding Tiles Path to success: ' + str(tileSolutions)))
#for i in range(len(missionSolutions)):
#        f.write(('\nMove#',i, missionSolutions[i], ':\n', missionSolutions[i][0:3], '\n', missionSolutions[i][3:6], '\n', missionSolutions[i][6:9]))

f.close()


