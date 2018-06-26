from task import Task

class HandInTask(Task):
    def __init__(self, agent, resource):
        Task.__init__(self, agent)
        self.r = resource

    def Execute(task, agent):
        chests = agent.block_list["chest"]
        chestLocation = (chests[0][0] + 0.5, 60, chests[0][1] + 0.5)
        raydat = agent.data.get(u'LineOfSight', False)

        if u'inventoriesAvailable' in agent.data:
            if (raydat and raydat[u'type'] == "chest" and raydat["inRange"]) or agent.MoveLookAtBlock(chestLocation):
                agent.SendCommand("move 0")
                # Adds items of a specified type to the chest
                if agent.AddItemsToChest(agent.data[u'inventory'], "chest", task.r):
                    agent.SendCommand("setPitch 0")
                    return True
        return False

