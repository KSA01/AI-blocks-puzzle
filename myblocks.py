
import random
import math
from util import GRID

def SOLVE(initial, goal):
    def GetPossibleMoves(state, goal): # Evaluation Function
        def GetPreviousBlock(block, goal):
            for stack in goal:
                for i in range(len(stack) - 1):
                    if stack[i+1] == block:
                        if not state.IsBlockUnderSomething(stack[i]):
                            return stack[i]
                        else:
                            return None
                        
        def CheckBlocks(goal):
            for stack in goal:
                for i in range(len(stack) - 1):
                    if not state.IsBlockUnderSomething(stack[i]) and not state.IsBlockUnderSomething(stack[i+1]):
                        if (i-1) >= 0:
                            if state.IsBlockOn(stack[i], stack[i-1]):
                                moves.append(('move', stack[i+1], stack[i]))

        moves = []
        misplaced_blocks = []

        for stack in goal:
            for i in range(len(stack) - 1):
                if not state.IsBlockOn(stack[i+1], stack[i]):
                    misplaced_blocks.append(stack[i+1])       # Gets a list of all misplaced blocks
        
        for block in misplaced_blocks:
            
            if state.IsBlockUnderSomething(block): # For all blocks misplaced and under something
                on_top = state.BlocksOnTop(block)
                if len(on_top) > 1:
                    on_top.reverse() # Reverse the list if contains more than 1 in order to work from the top block on the stack downward
                for b in on_top:
                    if not state.IsBlockOnTable(b):
                        prior_block = GetPreviousBlock(b, goal)
                        if prior_block is not None and not state.IsBlockUnderSomething(prev_block) and prior_block not in misplaced_blocks:
                            moves.append(('move', b, prior_block)) # Will move a block to where it should be if the correct block location is not under something and not misplaced
                        else:
                            moves.append(('move', b, 'Table')) # Otherwise it will move selected block to table
                            
            else:
                if not state.IsBlockOnTable(block): # For all blocks misplaced but not under something
                    prev_block = GetPreviousBlock(block, goal)
                    if prev_block is not None and not state.IsBlockUnderSomething(prev_block):
                        moves.append(('move', block, prev_block)) # If block is misplaced and its correct location block is available
                    else:
                        moves.append(('move', block, 'Table'))
                        if block in misplaced_blocks:
                            misplaced_blocks.remove(block) # Otherwise move selected block to table

        for stack in goal: # If the next block is on table, move it to the correct block now
            for i in range(len(stack) - 1):
                if state.IsBlockOnTable(stack[i+1]):
                    moves.append(('move', stack[i+1], stack[i]))  # Move the next block onto the current block

        #print(misplaced_blocks)
        return moves

    # Create a new puzzle with the initial arrangement
    puzzle = initial

    # Define the goal state
    goal_state = GRID(goal)

    # Create an empty path
    path = []

    # Get a copy of the initial puzzle state
    state = puzzle.GetCopy()

    # Loop until the puzzle is solved or we can't make any more moves
    while not goal_state.IsGoal(state.GetArraingement()) and len(path) < len(puzzle.grid) * len(puzzle.grid) * 2:
        # get the list of possible moves from the current state
        moves = GetPossibleMoves(state, goal)

        # If there are no possible moves, break out of the loop
        if not moves:
            break

        # Add the move to the path
        for move in moves:
            move_copy = move[1:] # Turns "('move', 'C', 'Table')" into "('C', 'Table')" so no errors when checking path
            path.append(move_copy)
            state.MoveBlock(move[1], move[2]) # Makes the move

    # If the puzzle was solved, return the path to check if correct
    if goal_state.IsGoal(state.GetArraingement()):
        return path

    # If the puzzle couldn't be solved, return an empty path
    return []
