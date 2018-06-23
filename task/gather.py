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
        resourceList = agent.block_list[task.r]
        location = (resourceList[0][0] + 0.5, 60, resourceList[0][1] + 0.5)
        task.reachedResource = agent.MoveLookAtBlock(location)
        raydat = agent.data.get(u'LineOfSight',False)
        print(location)
        
        if raydat and raydat[u'type'] == task.r and raydat["inRange"] :
            "Tree detected"
            if u'inventory' in agent.data:
                inv = [InventoryObject(**k) for k in agent.data[u'inventory']]
                agent.EquipToolForResource(task.r, inv)
            agent.SendCommand("attack 1")
            agent.SendCommand("yaw 0")
            agent.SendCommand("pitch 0")
        elif task.reachedResource and raydat[u'type'] == task.r:
            agent.SendCommand("attack 1")
        elif task.reachedResource and not raydat[u'type'] == task.r:
            agent.SendCommand("attack 0")
            agent.SendCommand("setPitch 0")
            return True
        else:
            agent.SendCommand("attack 0")

        return False
    
   

