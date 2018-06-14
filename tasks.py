from __future__ import print_function
from agent import Agent

# ==============================================================================
# ============================ Do tasks from queue =============================
# ==============================================================================

"""   Makes the given agent perform the current task from its tasklist
      Returns true when the task is done and removed from the queue
"""
def doCurrentTask(agent, data):
    if len(agent.taskList) > 0: # Look for tasks
        task = agent.taskList[0]
        if task[0](*task[1:], agent = agent, data = data): #Perform the task and remove the task from the queue if its finished
            del agent.taskList[0] 
            return True # Task is done and removed 
    return False #Not doing a task / task is not done yet 

"""
      Add a task to the agents task list
	  Tasks are in the form of (functionCall(), paramA, paramB)
"""
def addTask(agent, task):
    agent.taskList.append(task)
		
# ==============================================================================
# ============================ Return items ====================================
# ==============================================================================
""" Return items of given type to a chest
    Returns True when the task is done
    Returns False when the task is not done yet
    This should deprecate the chesterReduced.py file
"""
def returnItems(itemtype, agent, data):   
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

