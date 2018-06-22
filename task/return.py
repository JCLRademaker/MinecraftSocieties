from task import Task

class ReturnTask(Task):
    def __init__(self, agent, resource):
        Task.__init__(self, agent)
        self.r = resource
        self.reachedHome

    def Execute(task, agent):
        if not task.reachedHome:    # Go home
            task.reachedHome = agent.MoveLookAtBlock(agent.home)
            return False
        else:   # Return items to chest
            # Get the observed grid
            blocks = agent.data.get(u'worldGrid', 0)
            
            # Scan for chests: 
            index = 0
            for b in blocks:
                index += 1
                if b == u'ender_chest':
                    break
                    
            # Move to the chest and use it
            if agent.MoveToRelBlock(index):
                if u'inventoriesAvailable' in agent.data:
                    # Adds items of a specified type to the chest
                    agent.AddItemsToChest(agent.data[u'inventoriesAvailable'], agent.data[u'inventory'], "enderchest", task.r)
                    agent.SendCommand("use 0")      
                    return True
            return False
            
