from task import Task
from collections import namedtuple

# Named tuple consisting of info on entities
EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')

class CollectTask(Task):
    def __init__(self, agent, resource):
        Task.__init__(self, agent)
        self.r = resource

    def Execute(task, agent):
        if "close_entities" in agent.data:
            entities = [EntityInfo(k["x"], k["y"], k["z"], k["name"], k.get("quantity")) for k in agent.data["close_entities"]] #Unpack the json into a tuple
            target = False
            
            for ent in entities:
                if ent.name == task.r:
                    target = True # Still entities to gather            
                    agent.MoveToLocation((ent.x, ent.y, ent.z))                     
                    break	
            
            if not target:
                agent.SendCommand("move 0")# Return if the task is done (no more target entities)    
                return True
        else:
            return True
                
        return False
