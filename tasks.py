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
def returnItems(itemtype, data, agent):   
    # Get the observed grid
    blocks = data.get(u'worldGrid', 0)
    
    # Scan for chests: 
    index = 0
    for b in blocks:
        index += 1
        if b == u'ender_chest':
            break
            
    # Move to the chest and use it
    if agent.MoveToRelBlock(index):
        agent.SendCommand("use 1")
        if u'inventoriesAvailable' in data:
            # Adds items of a specified type to the chest
            agent.AddItemsToChest(data[u'inventoriesAvailable'], data[u'inventory'], "enderchest", itemtype)
            return True
    return False

# ==============================================================================
# ============================ Gather items ====================================
# ==============================================================================

# ==============================================================================
# ============================== Scout =========================================
# ==============================================================================

# ==============================================================================
# ============================ Build house =====================================
# ==============================================================================

