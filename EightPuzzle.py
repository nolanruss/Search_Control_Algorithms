import random

class EightPuzzle():
    def __init__(self):
        # Goal of game.
        self.goals = set([(1,2,3,8,0,4,7,6,5)])
        self.start = [1,2,3,8,0,4,7,6,5]

    def gen_start(self):
        self.start = [1,2,3,8,0,4,7,6,5]
        newStart = set()
        new = list(self.start)
		# Generate legal states and randomly select a start state.
        for i in range(50):
            parent, possible_moves = self.gen_moves(new)
            for move in possible_moves:
                newStart.add(move)
			# Select randomly from child states to generate new moves.
            new = possible_moves[random.randrange(0,len(possible_moves))]
		# Select the new start state, randomly breaking.
        for line in newStart:
            self.start = line
            if tuple(self.start) not in self.goals:
                if random.randrange(0,50) == 0:
                    break
        print('\nNew Start: ', self.start, '\n')
        if tuple(self.start) not in self.goals:
            return self.start
        else:
            print('Goal state used:')
            return self.gen_start()

    '''
    Finds all possible moves for key 0 in the start state and returns
    moves_index.

    '''
    def find_moves(self, start):
        children = [] # The list of possible moves from the start state.
        zero_index = 0 # Zero index stores index of the blank tile (0) position.
        moves_index = [] # Stores the index of each possible move.
        
        for i in range(len(start)):
            if start[i] == 0:
                zero_index = i # Find the index of element 0.

        # Find left, right, top, and bottom tiles for swapping if they exist.
        if zero_index % 3 > 0: # Find the left board tile index.
            moves_index.append(zero_index-1)
        if zero_index % 3 < 2: # Find the right board tile index.
            moves_index.append(zero_index+1)
        if zero_index > 2: # Find the upper board tile index.
            moves_index.append(zero_index-3)
        if zero_index < 6: # Find the lower board tile index.
            moves_index.append(zero_index+3)
        print('moves_index ', moves_index)
        return moves_index

    '''
    Generates moves based on the rules of the eight puzzle game.

    '''
    def gen_moves(self, start):
        moves_index = self.find_moves(list(start)) # Find the moves and store in a list.
        children = []
        zero_index = 0

        for i in range(len(start)):
            if start[i] == 0:
                zero_index = i

        for i in moves_index: # Generate all children with 0 tile swap.
            # Assign the start state to the current move.
            move = list(start)

            # Swap the 0 tile with the ith possible tile.
            move[i], move[zero_index] = move[zero_index], move[i]

            # Append each move state to the children list.
            children.append(tuple(move))

        # Return start as a tuple so it may be used as a key in a dict and
        # return the list of children states generated by this method.
        return tuple(start), children


    '''
    Getter method that returns the goal state of the eight puzzle game.

    '''
    def get_goals(self):
        return self.goals