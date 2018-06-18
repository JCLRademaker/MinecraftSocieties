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

# ==============================================================================
# ============================== Scout =========================================
# ==============================================================================

# ==============================================================================
# ============================ Build house =====================================
# ==============================================================================

