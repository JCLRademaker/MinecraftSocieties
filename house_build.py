from __future__ import print_function

from builtins import range
import MalmoPython
import os
import sys
import time
import random
import json
import errno
import math

from agent import Agent
from collections import namedtuple

# Named tuple consisting of info on entities
EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')

# Create a named tuple type for the inventory contents.
InventoryObject = namedtuple('InventoryObject', 'type, colour, variant, quantity, inventory, index')
InventoryObject.__new__.__defaults__ = ("", "", "", 0, "", 0)

# Mapping from which resources can be gathered by which tools
resourceToToolMapping = { u'log' : "iron_axe"}


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
  </ServerSection>
  <AgentSection mode="Survival">
    <Name>Walker</Name>
    <AgentStart>
      <Placement x="0" y="227.0" z="0" pitch="0" yaw="0"/>
      <Inventory>
          <InventoryItem slot="1" type="iron_axe"/>
          <InventoryItem slot="2" type="iron_pickaxe"/>
          <InventoryItem slot="3" type="log" quantity="64"/>
      </Inventory>
    </AgentStart>
    <AgentHandlers>
        
       <ObservationFromFullInventory flat="false"/>
       <InventoryCommands/>
       <ContinuousMovementCommands/>
       <AbsoluteMovementCommands/>
       <ObservationFromFullStats/>
		<ObservationFromNearbyEntities>
			<Range name="close_entities" xrange="5" yrange="5" zrange="5" update_frequency="1" />
        </ObservationFromNearbyEntities>
       <ObservationFromGrid>
            <Grid name="close_grid" absoluteCoords="false">
                <min x="-6" y="0" z="-6"/>
                <max x="6" y="0" z="6"/>
            </Grid>
            <Grid name="small_grid" absoluteCoords="false">
                <min x="-1" y="-1" z="-1"/>
                <max x="1" y="-1" z="1"/>
            </Grid>
        </ObservationFromGrid>
    </AgentHandlers>
  </AgentSection>  
  
</Mission>'''

# ==============================================================================
# =========================== Initializing the Agent ===========================
# ==============================================================================

agent = Agent(xml)
agent.StartMission()

# ==============================================================================
# =========================== Implementing the Agent ===========================
# ==============================================================================


# Loop until mission ends:

while agent.is_mission_running():
   success, data = agent.Observe()
   if success:

       inv = data.get(u'inventory',0)
       #print(inv[u'type'])
       
       #select wood from inventory
       #if inv[u'type'][0] != u'log':
       agent.SendCommand("hotbar.4 1")
       agent.SendCommand("hotbar.4 0")                                       
        
       grid = data.get(u'small_grid', 0)
       
       index = 0
       
       #==============================
       #fill a 3x3 grid with wood (center should be empty as the agent stays inside)
       #==============================

       #iterate through the edges of the grid
       #ignore pos 4 (middle position where agent is)
       for elem in grid:
          if index == 0 or index == 2 or index == 6 or index == 8:
             if agent.MoveToRelBlock(index): #move and look at the block
                agent.SendCommand("use 1")   #build wood inside block
                index += 1
          else:
             index += 1
       
       #iterate through the 3 remaining positions
       for elem in grid:
          if index == 1 or index == 3 or index == 5 :
             if agent.MoveToRelBlock(index): #move and look at the block
                agent.SendCommand("use 1")   #build wood inside block
                index += 1
          else:
             index += 1
      

                


print()
print("Mission ended")
# Mission has ended.
