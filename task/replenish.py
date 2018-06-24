from task import Task
from collections import namedtuple

class ReplenishTask(Task):
    def __init__(self, agent):
        Task.__init__(self, agent)
        self.Inventory = agent.GetInventory(agent.data[u'inventory'], "inventory")
        self.Chest = agent.GetInventory(agent.data[u'inventory'], "chest")
        self.GotMelons = False

    def Execute(task, agent):
        chests = agent.block_list["chest"]
        chestLocation = (chests[0][0] + 0.5, 60, chests[0][1] + 0.5)
        
        if (not task.GotMelons) and agent.MoveLookAtBlock(chestLocation): # get melons
            if agent.GetAmountOfType(task.Inventory, "melon") == 0:
                task.GotMelons = agent.AddItemsToInv(agent.data[u'inventory'], "chest", "melon", 1)
            else:
                task.GotMelons = True
        elif task.GotMelons:                                              # eat melons
            if agent.MoveLookAtBlock(agent.home):
                for item in task.Inventory:
                    if item.type == "melon":
                        itemIndex = item.index + 1
                        agent.SendCommand("hotbar." + str(itemIndex) + " 1")
                        agent.SendCommand("hotbar." + str(itemIndex) + " 0")
                
                if int(agent.data[u'Food']) >= 20:
                    agent.SendCommand("use 0")
                    agent.AddItemsToChest(agent.data[u'inventory'], "inventory", "melon")
                    return True
                else:
                    agent.SendCommand("use 1")
