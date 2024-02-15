
from util import GRID
from myblocks import SOLVE
import time

def RunTest(initial, goal):
    print("Test:", initial, goal)
    grid = GRID(initial)
    begin = time.time()
    solution = SOLVE(grid, goal)
    thetime = time.time() - begin
    print("Time to Compute: " + str(thetime))
    print("Proposed Solution:", solution)
    print("Solution Steps:", str(len(solution)))
    result = GRID(initial).VerifyPath(goal, solution)
    print("Solution Correct" if result else "Invalid Path")

begin = time.time()
RunTest([["B"], ["A", "C"]], [["C","B","A"]]) #3

initial = [["A", "B", "C"], ["D", "E"]]
RunTest(initial, [["A", "C"], ["D", "E", "B"]]) #3
RunTest(initial, [["A", "B", "C", "D", "E"]]) #3
RunTest(initial, [["D", "E", "A", "B", "C"]]) #5
RunTest(initial, [["C", "D"], ["E", "A", "B"]]) #6

thetime = time.time() - begin
print("Time to Compute Everything: " + str(thetime))