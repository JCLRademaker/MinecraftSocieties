from task import Task
from collections import namedtuple

class ReplenishTask(Task):
    def __init__(self, agent):
        Task.__init__(self, agent)
        self.GotMelons = False
        self.doneEating = False

    def Execute(task, agent):
        chests = agent.block_list["chest"]
        chestLocation = (chests[0][0] + 0.5, 60, chests[0][1] + 0.5)
        inventory = agent.GetInventory(agent.data[u'inventory'], "inventory")  # eat melons
        
        if (not task.GotMelons) and agent.MoveLookAtBlock(chestLocation): # get melons
            if agent.GetAmountOfType(inventory, "melon") == 0:
                task.GotMelons = agent.AddItemsToInv(agent.data[u'inventory'], "chest", "melon", 1)
        elif task.GotMelons:
            if not task.doneEating and agent.MoveLookAtBlock(agent.home):
                for item in inventory:
                    if item.type == "melon":
                        itemIndex = item.index + 1
                        agent.SendCommand("hotbar." + str(itemIndex) + " 1")
                        agent.SendCommand("hotbar." + str(itemIndex) + " 0")
                
                if int(agent.data[u'Food']) >= 20:
                    print("Ik ben klaar met eten hoe kan dit nou")
                    agent.SendCommand("use 0")
                    task.doneEating = True
                else:
                    agent.SendCommand("use 1")

            if task.doneEating and agent.MoveLookAtBlock(chestLocation):
                agent.AddItemsToChest(agent.data[u'inventory'], "chest", "melon")
                return True
