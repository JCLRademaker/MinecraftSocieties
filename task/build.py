import Task

class BuildTask(Task):
    def __init__(self, agent, location):
        Task.__init__(self, agent)
        self.l = location

        self.working = [False]*15
        self.working[0] = True
        self.CalcHouseGrid()

        self.CalcRoof(self.l)
        self.workingR = [False] * len(self.roof)
        self.workingR[0] = True

        self.inrange = False


    def CalcHouseGrid(self):
        self.grid = self.calcHouseLevel((self.l[0], self.l[1], self.l[2]))
        self.grid += self.calcHouseLevel((self.l[0], self.l[1]+1, self.l[2]))
        self.grid += (self.l[0] + 0, self.l[1], self.l[2] + 0),

        return self.grid

    def CalcRoof(self, location):
        self.roof = [
            (location[0]+1, location[1], location[2]+2),
            (location[0]+0, location[1], location[2]+2),
            (location[0]-1, location[1], location[2]+2),

            (location[0]+1, location[1]+1, location[2]+1),
            (location[0]+0, location[1]+1, location[2]+1),
            (location[0]-1, location[1]+1, location[2]+1),

            (location[0]+1, location[1], location[2]+1),
            (location[0]-1, location[1], location[2]+0),
            ]
        return self.roof

    def calcHouseLevel(self, location):
        grid = [
            (location[0]+1, location[1], location[2]-1),
            (location[0]+1, location[1], location[2]+1),
            (location[0]-1, location[1], location[2]+1),
            (location[0]-1, location[1], location[2]-1),
            (location[0]+0, location[1], location[2]+1),
            (location[0]-1, location[1], location[2]+0),
            (location[0]+1, location[1], location[2]+0),
            ]
        return grid

    def Execute(task, agent):
        """  """
        location = (task.l[0]+0.5,task.l[1],task.l[2]+0.5)

        if task.inrange:
            for i, l in enumerate(task.grid):
                if i > 7:
                    print (task.working)
                if not task.working[i]:
                    continue
                elif agent.PlaceBlock(l):
                    task.working[i+1] = True

            if all(task.working):
                return True
        else:
            task.inrange = agent.MoveToLocation(location, 0.2)
        return False



# x
# [[+-][+0][++]]
# [[0-][00][0+]]
# [[--][-0][-+]]
#           z
