from __future__ import print_function

from tools import spatial


from builtins import range
import MalmoPython
import os
import sys
import time
import random
import json
import errno
import math
import malmoutils

from collections import namedtuple

from multiagent import multiserver, createAgentXML

malmoutils.fix_print()

invent =  '''<InventoryItem slot="1" type="iron_axe"/>
          <InventoryItem slot="2" type="iron_pickaxe"/>
          <InventoryItem slot="3" type="log" quantity="64"/>'''

logX = -2
logZ = -1
 # -- set up the mission --
xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <About>
    <Summary/>
  </About>
  <ServerSection>
    <ServerInitialConditions>
      <Time>
        <StartTime>0</StartTime>
      </Time>
    </ServerInitialConditions>
    <ServerHandlers>
      <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" seed="" forceReset = "1"/>
       <DrawingDecorator>
 		<DrawBlock x="''' + str(logX) + '''"  y="227" z="'''+ str(logZ) +'''" type="log"/>
       </DrawingDecorator>

      <ServerQuitFromTimeUp description="" timeLimitMs="35000"/>
      <ServerQuitWhenAnyAgentFinishes description=""/>
    </ServerHandlers>
  </ServerSection>'''+ createAgentXML.CreateAgentXML("Walker", inventory = invent) + '''

</Mission>'''

# ==============================================================================
# =========================== Initializing the Agent ===========================
# ==============================================================================

agentNames = ["Walker"]

server = multiserver.MultiServer(xml)
server.StartServer(agentNames)

# ==============================================================================
# =========================== Implementing the Agent ===========================
# ==============================================================================


# x,y = all x,y | x*x + y*y < 3

def GetGrid(x, y, z):
    gr = []
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            ind = spatial.IndexFromDifference((dx,0,dz))-1
            gr.append(ind)
    return gr

grid = GetGrid(0,228, 0)
server.agents[0].SendCommand("hotbar.4 1")
server.agents[0].SendCommand("hotbar.4 0")

i = 0
working = grid[i]

while server.IsRunning():
    observes = server.Observe()
    if observes[0][0]:
        pos = server.agents[0].Position

        # Inventory
        inv = observes[0][1].get(u'inventory', 0)

        # The blocks around the agent
        blocks = observes[0][1].get(u'worldGrid', 0)

        # Place the blocks
        #for i in range(len(grid)):
        if blocks[working] == u"log":
            print("placed", i)
            i += 1
            working = grid[i]
            continue
        else:
            loc = spatial.LocationFromIndex(server.agents[0].Position, working)
            loc = (loc[0],loc[1]-1,loc[2])
            if server.agents[0].LookAtBlock(loc):
                server.agents[0].SendCommand("use 1")
                server.agents[0].SendCommand("use 0")
