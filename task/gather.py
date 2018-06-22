from task import Task

class GatherTask(Task):
    def __init__(self, agent, resource):
        Task.__init__(self, agent)
        self.r = resource
        self.reachedResource = False

    def Execute(task, agent):
        if not task.reachedResource:    # go to know resource spot
            resourceList = agent.block_list[resource]
            location = resourceList[0]
            task.reachedResource = agent.MoveLookAtBlock(location)    
            return False
        elif "worldGrid" in agent.data:  # harvest resource
            blocks = agent.data.get(u'worldGrid', 0)
            index = 0
            target = False      
                        
            # Scout the grid for the given resource
            for b in blocks:
                index += 1
                if b == task.r:   
                    target = True       
                    if u'inventory' in agent.data:
                        inv = [InventoryObject(**k) for k in agent.data[u'inventory']]
                        agent.EquipToolForResource(self.r, inv)
                    break								
            
            # If resource found, harvest it otherwise stop attacking
            if target:
                if agent.MoveToRelBlock(index):
                    agent.SendCommand("attack 1")
            else:
                agent.SendCommand("attack 0")

            return not target                    
        return False
    
   

