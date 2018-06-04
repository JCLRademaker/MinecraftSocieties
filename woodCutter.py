from __future__ import print_function

from builtins import range
from agent import Agent

import MalmoPython
import os
import sys
import time
import random
import json
import errno
import math
from collections import namedtuple

# Named tuple consisting of info on entities
EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')

# Create a named tuple type for the inventory contents.
InventoryObject = namedtuple('InventoryObject', 'type, colour, variant, quantity, inventory, index')
InventoryObject.__new__.__defaults__ = ("", "", "", 0, "", 0)
  
# Coordinates to randomly spawn a tree on  
logX = -4
logZ = -1

logXX = -2
logZZ = 2

logXXX = 3
logZZZ = 3   
  
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
		<DrawBlock x="''' + str(logXX) + '''"  y="227" z="'''+ str(logZZ) +'''" type="log"/>	
		<DrawBlock x="''' + str(logXXX) + '''"  y="227" z="'''+ str(logZZZ) +'''" type="log"/>
        <DrawEntity x="10" y="227" z="10" type="MinecartRideable"/>
        <DrawItem x="0" y="227" z="10" type="cookie"/>
      </DrawingDecorator>
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
      </Inventory>
    </AgentStart>
    <AgentHandlers>
        <ObservationFromFullInventory flat="false"/>
        <InventoryCommands/>
	    <ContinuousMovementCommands/>
		<DiscreteMovementCommands/>
		<AbsoluteMovementCommands/>
	    <ObservationFromFullStats/>
		<ObservationFromNearbyEntities>
			<Range name="close_entities" xrange="5" yrange="1" zrange="5" update_frequency="1" />
        </ObservationFromNearbyEntities>
	  	<ObservationFromGrid>
            <Grid name="tree_stumps" absoluteCoords="false">
                <min x="-6" y="0" z="-6"/>
                <max x="6" y="0" z="6"/>
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
while agent.is_mission_running:
    succes, data = agent.Observe()
    if succes:
		#Detect the items of a certain type(for now logs), orientate towards it and pick it up
        if "close_entities" in data:
            entities = [EntityInfo(k["x"], k["y"], k["z"], k["name"], k.get("quantity")) for k in data["close_entities"]] #Unpack the json into a tuple
            for ent in entities:
                if ent.name == "log":
                
                    # Enter the collecting state, stop attacking, look forward
                    agent.isCollecting = True
                    agent.SendCommand("attack 0")  
                    agent.SendCommand("setPitch 0")					
                    agent.MoveToLocation(ent.x, ent.y, ent.z)                    
                    break	
                
                # Exit the collecting state and stop movement        
                agent.isCollecting = False	
                agent.SendCommand("move 0")					
        
        #Detect nearby treestumps, and if we are not collecting items proceed to harvest the stump
        if "tree_stumps" in data and not agent.isCollecting:
            
            #Get the observed grid
            blocks = data.get(u'tree_stumps', 0)
            index = 0
			
            #Scan the grid for treestumps and equip the correct tool
            for b in blocks:
                index += 1
                if b == u'log':     
                    if u'inventory' in data:
                        inv = [InventoryObject(**k) for k in data[u'inventory']]
                        agent.EquipToolForResource(u'log', inv)
                    break								

            if agent.MoveToRelative(index):
                    agent.SendCommand("attack 1")         

print()
print("Mission ended")
# Mission has ended.
