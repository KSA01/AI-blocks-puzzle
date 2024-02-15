
import numpy as np

class GRID:
    def __init__(self, arrangement):
        self.grid = {}
        for stck in arrangement:
            parent = None
            for i in range(len(stck)):
                if i == len(stck) - 1:
                    self.grid[stck[i]] = (parent, None)
                    break
                self.grid[stck[i]] = (parent, stck[i+1])
                parent = stck[i]

    def MoveBlock(self, name, to_loc): # to_loc: string of block it is on or "Table"
        if not name in self.grid:
            print("block not found")
            return False
        if self.grid[name][1] is not None:
            print("block can't be moved")
            return False

        if to_loc == "Table" or to_loc == " Table":
            pass
        elif not to_loc in self.grid:
            print("target block not found")
            return False
        elif self.grid[to_loc][1] is not None:
            print("target block occupied")
            return False

        if self.grid[name][0] is None: # is on the Table
            if to_loc == "Table" or to_loc == " Table":
                pass
            else:
                self.grid[name] = (to_loc, None)
                self.grid[to_loc] = (self.grid[to_loc][0], name)
        else:
            self.grid[self.grid[name][0]] = (self.grid[self.grid[name][0]][0], None)
            if to_loc == "Table" or to_loc == " Table":
                self.grid[name] = (None, None)
            else:
                self.grid[name] = (to_loc, None)
                self.grid[to_loc] = (self.grid[to_loc][0], name)

        return True
    
    def IsGoal(self, arrangement):
        for stck in arrangement:
            for i in range(len(stck)):
                if not stck[i] in self.grid:
                    return False
                if i == 0:
                    if self.grid[stck[i]][0] is not None:
                        return False
                    
                if i == len(stck) - 1:
                    if self.grid[stck[i]][1] is not None:
                        return False
                else:
                    if self.grid[stck[i]][1] != stck[i+1]:
                        return False
        return True
    
    def VerifyPath(self, goal, path): # path: list of (name, to_loc) pairs
        for p in path:
            if not self.MoveBlock(*p):
                return False
        return self.IsGoal(goal)
    
    def IsBlockOn(self, block, location): # location: other block or "Table"
        if not block in self.grid:
            return False
        if location == "Table" or location == " Table":
            return self.grid[block][0] == None
        return self.grid[block][0] == location
    
    def IsBlockOnTable(self, block):
        if not block in self.grid:
            return False
        return self.grid[block][0] == None
    
    def IsBlockUnderSomething(self, block):
        if not block in self.grid:
            return False
        return self.grid[block][1] is not None
    
    def BlockStackedHowHigh(self, block): # 0 = on table, 1 = on one block, etc.
        count = -1
        while block is not None:
            if not block in self.grid:
                return -1
            count += 1
            block = self.grid[block][0]
        return count
    
    def CountStackedOnTop(self, block): # how many blocks stack on this one
        count = -1
        while block is not None:
            if not block in self.grid:
                return -1
            count += 1
            block = self.grid[block][1]
        return count
    
    def BlocksUnder(self, block): # returns list of blocks under this one
        lst = []
        if not block in self.grid:
            return None
        block = self.grid[block][0]
        while block is not None:
            if not block in self.grid:
                return None
            lst.append(block)
            block = self.grid[block][0]
        return lst
    
    def BlocksOnTop(self, block): # returns list of block on top of this one
        lst = []
        if not block in self.grid:
            return None
        block = self.grid[block][1]
        while block is not None:
            if not block in self.grid:
                return None
            lst.append(block)
            block = self.grid[block][1]
        return lst
    
    def GetArraingement(self):
        result = []
        for k in list(self.grid.keys()):
            if self.grid[k][0] is not None:
                continue
            p = k
            m = []
            while p:
                m.append(p)
                p = self.grid[p][1]
            result.append(m)
        return result

    def GetCopy(self):
        g = GRID([])
        g.grid = self.grid.copy()
        return g
    
    def __str__(self):
        return str(self.grid)
