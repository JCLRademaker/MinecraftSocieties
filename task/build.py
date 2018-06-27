from task import Task

class BuildTask(Task):
    def __init__(self, agent, location):
        Task.__init__(self, agent)
        self.GotWood = False
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
        raydat = agent.data.get(u'LineOfSight', False)

        for i in range(1000):
            i += 1

        inventory = agent.GetInventory("inventory")  # get wood

        if u'inventoriesAvailable' in agent.data:
            if not task.GotWood and ((raydat and raydat[u'type'] == "chest" and raydat["inRange"]) or
                                     agent.MoveLookAtBlock(agent.chest_location)):
                if agent.GetAmountOfType(inventory, "log") == 0:
                    for inv in agent.data[u'inventoriesAvailable']:
                        if inv[u'name'] == "chest":
                            task.GotWood = agent.AddItemsToInv(agent.data[u'inventory'], "chest", "log", 1)

        if task.GotWood:
            for item in inventory:
                if item.type == "log":
                    itemIndex = item.index + 1
                    agent.SendCommand("hotbar." + str(itemIndex) + " 1")
                    agent.SendCommand("hotbar." + str(itemIndex) + " 0")

            """  """
            location = (task.l[0]+0.5, task.l[1], task.l[2]+0.5)

            if task.inrange:
                for i, l in enumerate(task.grid):
                    if not task.working[i]:
                        continue
                    elif agent.PlaceBlock(l):
                        task.working[i+1] = True

                if all(task.working):
                    return True
            else:
                task.inrange = agent.MoveToLocation(location, 0.2)
            return False

        return False



# x
# [[+-][+0][++]]
# [[0-][00][0+]]
# [[--][-0][-+]]
#           z
