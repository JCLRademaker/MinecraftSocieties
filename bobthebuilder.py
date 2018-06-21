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

      <ServerQuitFromTimeUp description="" timeLimitMs="35000"/>
      <ServerQuitWhenAnyAgentFinishes description=""/>
    </ServerHandlers>
  </ServerSection>'''+ createAgentXML.CreateAgentXML("Walker", inventory = invent, coords = (0, 227, 0)) + '''

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

def CGetGrid(x,y,z, size=1):
    c1 = (x-size,y,z-size)
    c2 = (x-size,y,z+size)
    c3 = (x+size,y,z+size)
    c4 = (x+size,y,z-size)

    size += 1

    gr = [c1, c2, c3, c4]

    for dx in range(x-size+1, x + size):
        for dz in range(z-size+1, z + size):
            gr.append((dx,y,dz))

    return gr

def GetGrid(x, y, z, size=1):
    c1 = spatial.IndexFromDifference((-size, 0, -size))
    c2 = spatial.IndexFromDifference((-size, 0,  size))
    c3 = spatial.IndexFromDifference(( size, 0,  size))
    c4 = spatial.IndexFromDifference(( size, 0,  -size))
    gr = [c1, c2, c3, c4]

    #for dx in range(-size, size+1):
    #    for dz in range(-size, size+1):
    #        ind = spatial.IndexFromDifference((dx,0,dz))-1
    #        gr.append(ind)
    return gr

grid = CGetGrid(0,227, 0)
print(grid)

server.agents[0].SendCommand("hotbar.4 1")
server.agents[0].SendCommand("hotbar.4 0")


while server.IsRunning():
    observes = server.Observe()
    if observes[0][0]:
        pos = server.agents[0].Position

        # Inventory
        inv = observes[0][1].get(u'inventory', 0)

        # The blocks around the agent
        blocks = observes[0][1].get(u'worldGrid', 0)

        if grid:
            working = grid[0]
            if server.agents[0].PlaceBlock(working):
                grid = grid[1:]
        else:
            # Determine if all blocks are placed:
            grid2 = []
            for i in grid:
                if not blocks[int(spatial.IndexFromLocation(server.agents[0].Position, i))] == u'log':
                    grid2.append(i)
            print(grid2)
            if grid2:
                grid = grid2
                i = 0
                working = grid[i]
            else:
                break
