from task import Task
import gather, collect, handIn, scout


class ReplenishTask(Task):
    def __init__(self, agent):
        Task.__init__(self, agent)
        self.GotMelons = False
        self.doneEating = False

    def Execute(task, agent):
        raydat = agent.data.get(u'LineOfSight', False)
        for i in range(1000):
            i += 1

        inventory = agent.GetInventory("inventory")

        if (not task.GotMelons) and ((raydat and raydat[u'type'] == "chest" and raydat["inRange"]) or
                                     agent.MoveLookAtBlock(agent.chest_location)):
            if agent.GetAmountOfType(inventory, "melon") == 0:
                agent.SendCommand("pitch 0")
                for inv in agent.data[u'inventoriesAvailable']:
                    if inv[u'name'] == "chest":
                        chest = agent.GetInventory("chest")
                        if agent.GetAmountOfType(chest, "melon") > 0:
                            task.GotMelons = agent.AddItemsToInv(agent.data[u'inventory'], "chest", "melon", 1)
                        # Gather resources
                        else:
                            resourceKBCount = 0
                            if u'melon_block' in agent.block_list:
                                resourceKBCount = len(agent.block_list[u'melon_block'])
                            if resourceKBCount > 0:  # We know there is a resource so mine it
                                agent.addTask(gather.GatherTask(agent, u'melon_block'))
                                agent.addTask(collect.CollectTask(agent, "melon"))
                                agent.addTask(handIn.HandInTask(agent, "melon"))
                                agent.SendMessage("No melons in the inventory! Going to gather melons.")
                            # We need to scout for the resource
                            else:
                                agent.SendMessage("No melons in my observation data! I am going to scout.")
                                agent.addTask(scout.ScoutTask(agent, agent.InformationCount() + 10))
                            agent.SendCommand("setPitch 0")
                            return True
            # There is already something in the inventory
            else:
                task.GotMelons = True
        # Select the melons in the hotbar and start munching
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
            # Put the melons back in the chest
            if task.doneEating and ((raydat and raydat[u'type'] == "chest" and raydat["inRange"]) or
                                    agent.MoveLookAtBlock(agent.chest_location)):
                agent.SendCommand("pitch 0")
                agent.AddItemsToChest(agent.data[u'inventory'], "chest", "melon")
                agent.SendCommand("setPitch 0")
                return True
