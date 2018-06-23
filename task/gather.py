from task import Task
from collections import namedtuple

# Create a named tuple type for the inventory contents.
InventoryObject = namedtuple('InventoryObject', 'type, colour, variant, quantity, inventory, index')
InventoryObject.__new__.__defaults__ = ("", "", "", 0, "", 0)

class GatherTask(Task):
    def __init__(self, agent, resource):
        Task.__init__(self, agent)
        self.r = resource
        self.reachedResource = False

    def Execute(task, agent):
        if not task.reachedResource:    # go to know resource spot
            resourceList = agent.block_list[task.r]
            location = (resourceList[0][0], 61, resourceList[0][1])
            task.reachedResource = agent.MoveToLocation(location,  distance = 4)
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
                        agent.EquipToolForResource(task.r, inv)
                    break								
            
            # If resource found, harvest it otherwise stop attacking
            if target:
                raydat = agent.data.get(u'LineOfSight',False)
                if raydat and raydat[u'type'] == task.r and raydat["inRange"] :
                    "Tree detected"
                    agent.SendCommand("attack 1")
                    agent.SendCommand("yaw 0")
                    agent.SendCommand("pitch 0")
                elif agent.MoveToRelBlock(index):
                    agent.SendCommand("attack 1")
                else:
                    agent.SendCommand("attack 0")   
            else:
                agent.SendCommand("attack 0")

            return not target                    
        return False
    
   

