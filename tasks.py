from __future__ import print_function
from agent import Agent
# ==============================================================================
# ============================ Return items ====================================
# ==============================================================================
""" Return items of given type to a chest
    Returns True when the task is done
    Returns False when the task is not done yet
    This should deprecate the chesterReduced.py file
"""
def returnItems(itemtype, agent):   
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
        agent.SendCommand("use 1")
        if u'inventoriesAvailable' in agent.data:
            # Adds items of a specified type to the chest
            agent.AddItemsToChest(agent.data[u'inventoriesAvailable'], agent.data[u'inventory'], "enderchest", itemtype)
            agent.SendCommand("use 0")      
            return True
    return False
  
""" Move the agent to its specified home coordinates"""   
def goHome(agent):
    return agent.MoveLookAtBlock(agent.home)    

# ==============================================================================
# ============================ Gather items ====================================
# ==============================================================================
""" Looks up a resource location in its memory and moves there"""
def moveToResource(resource, agent):
    resourceList = agent.block_list[resource]
    location = resourceList[0]
    return agent.MoveLookAtBlock(location)    

""" 
Look for the given resource in your vicinity grid
If there is none, target will be false and the task is done
If there is, walk towards it and harvest it
"""
def harvestResource(resource, agent):
    if "world_grid" in agent.data:
        blocks = agent.data.get(u'world_grid', 0)
        index = 0
        target = False
        
        # Scout the grid for the given resource
        for b in blocks:
            index += 1
            if b == resource:   
                target = True            
                if u'inventory' in agent.data:
                    inv = [InventoryObject(**k) for k in agent.data[u'inventory']]
                    agent.EquipToolForResource(resource, inv)
                break								
        
        # If resource found, harvest it otherwise stop attacking
        if target:
            if agent.MoveToRelBlock(index):
                agent.SendCommand("attack 1")
        else:
            agent.SendCommand("attack 0")

        return not target                    

"""
Scavenges the ground for harvested resources to collect
Resource entity might have a different name than the resource block (does not always have to hold)
"""      
def collectResource(resourceEntity, agent):
    if "close_entities" in agent.data:
        entities = [EntityInfo(k["x"], k["y"], k["z"], k["name"], k.get("quantity")) for k in agent.data["close_entities"]] #Unpack the json into a tuple
        target = False
        
        for ent in entities:
            if ent.name == resourceEntity:
                target = True # Still entities to gather            
                agent.MoveLookAtLocation((ent.x, ent.y, ent.z))                     
                break	
        
        return not target # Return if the task is done (no more target entities)    
          
# ==============================================================================
# ============================== Scout =========================================
# ==============================================================================

# ==============================================================================
# ============================ Build house =====================================
# ==============================================================================

