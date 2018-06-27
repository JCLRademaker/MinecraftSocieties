from task import Task
from collections import namedtuple

class ReplenishTask(Task):
    def __init__(self, agent):
        Task.__init__(self, agent)
        self.GotMelons = False
        self.doneEating = False

    def Execute(task, agent):
        for i in range(1000):
            i += 1

        inventory = agent.GetInventory("inventory")  # eat melons

        if (not task.GotMelons) and agent.MoveLookAtBlock(agent.chest_location):  # get melons
            if agent.GetAmountOfType(inventory, "melon") == 0:
                for inv in agent.data[u'inventoriesAvailable']:
                    if inv[u'name'] == "chest":
                        task.GotMelons = agent.AddItemsToInv(agent.data[u'inventory'], "chest", "melon", 1)
            else:
                task.GotMelons = True
        elif task.GotMelons:
            if not task.doneEating and agent.MoveLookAtBlock(agent.home):
                for item in inventory:
                    if item.type == "melon":
                        itemIndex = item.index + 1
                        agent.SendCommand("hotbar." + str(itemIndex) + " 1")
                        agent.SendCommand("hotbar." + str(itemIndex) + " 0")
                
                if int(agent.data[u'Food']) >= 20:
                    agent.SendCommand("use 0")
                    task.doneEating = True
                else:
                    if agent.GetAmountOfType(inventory, "melon") == 0:
                        return True
                    agent.SendCommand("use 1")

            if task.doneEating and agent.MoveLookAtBlock(agent.chest_location):
                agent.AddItemsToChest(agent.data[u'inventory'], "chest", "melon")
                agent.SendCommand("setPitch 0")
                return True
