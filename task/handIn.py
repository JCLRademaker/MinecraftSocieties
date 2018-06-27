from task import Task

class HandInTask(Task):
    def __init__(self, agent, resource):
        Task.__init__(self, agent)
        self.r = resource

    def Execute(task, agent):
        raydat = agent.data.get(u'LineOfSight', False)

        if u'inventoriesAvailable' in agent.data:
            if (raydat and raydat[u'type'] == "chest" and raydat["inRange"]) or \
                    agent.MoveLookAtBlock(agent.chest_location):

                for inv in agent.data[u'inventoriesAvailable']:
                    if inv[u'name'] == "chest":
                        agent.SendCommand("setPitch 0")
                        # Adds items of a specified type to the chest
                        if agent.AddItemsToChest(agent.data[u'inventory'], "chest", task.r):
                            # chest = agent.GetInventory("chest")
                            agent.SendCommand("move 0")
                            agent.SendCommand("setPitch 0")

                            # Update resources for reasoning
                            agent.melons_in_chest = agent.GetAmountOfType(agent.chest, "melon")
                            agent.wood_in_chest = agent.GetAmountOfType(agent.chest, "wood")
                            return True
        return False

