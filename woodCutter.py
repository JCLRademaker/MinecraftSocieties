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
from collections import namedtuple

# Named tuple consisting of info on entities
EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')

# Create a named tuple type for the inventory contents.
InventoryObject = namedtuple('InventoryObject', 'type, colour, variant, quantity, inventory, index')
InventoryObject.__new__.__defaults__ = ("", "", "", 0, "", 0)


isCollecting = False

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)
  
# Coordinates to randomly spawn a tree on  
logX = -4
logZ = -1

logXX = -2
logZZ = 2

logXXX = 4
logZZZ = 3

# Mapping from which resources can be gathered by which tools
resourceToToolMapping = { u'log' : "iron_axe"}

#Calculate the angle towards our target
def calcYawToBlock(objectx, objectz, agentx, agentz):
	dx = objectx - agentx
	dz = objectz - agentz
	yaw = -180 * math.atan2(dx, dz) / math.pi
	return yaw

#Calculate the angle towards our target
def calcYawToEntity(entity, x, y, z):
	dx = entity.x - x
	dz = entity.z - z
	yaw = -180 * math.atan2(dx, dz) / math.pi
	return yaw

def pathag(sidea, sideb):
    csquare = (sidea ** 2) + (sideb ** 2)
    sidec = math.sqrt(csquare)
    return sidec
    
def tryEquipItem(itemName):
    test = "ik neuk jullie allemaal de moeder" 

    
  
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

my_mission = MalmoPython.MissionSpec(xml,True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
#print(block_types)
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')

# Loop until mission ends:
while world_state.is_mission_running:
    world_state = agent_host.getWorldState()
    if world_state.number_of_observations_since_last_state > 0:
        
        # Read the agent position and yaw from the observations
        msg = world_state.observations[-1].text
        data = json.loads(msg)		
        current_x = data.get(u'XPos', 0)
        current_z = data.get(u'ZPos', 0)
        current_y = data.get(u'YPos', 0)
        yaw = data.get(u'Yaw', 0)		
        pitch = data.get(u'Pitch', 0)	
		
		#Detect the items of a certain type(for now logs), orientate towards it and pick it up
        if "close_entities" in data:
            entities = [EntityInfo(k["x"], k["y"], k["z"], k["name"], k.get("quantity")) for k in data["close_entities"]] #Unpack the json into a tuple
            for ent in entities:
                if ent.name == "log":
                
                    # Enter the collecting state, stop attacking, look forward
                    isCollecting = True
                    agent_host.sendCommand("attack 0")  
                    agent_host.sendCommand("setPitch 0")
                    
                    #Calculate the yaw needed to orientate towards the item
                    newYaw = calcYawToEntity(ent, current_x, current_y, current_z)
                    deltaYaw = newYaw - yaw
                    
                    # If we arent facing the item yet we rotate, otherwise start moving towards it
                    if abs(deltaYaw) > 2:
						while deltaYaw < -180:
							deltaYaw += 360;
						while deltaYaw > 180:
							deltaYaw -= 360;
						deltaYaw /= 90.0;
						# Turn the agent
						agent_host.sendCommand("turn " + str(deltaYaw))
                    else:
						agent_host.sendCommand("move 1")
                    break	
                
                # Exit the collecting state and stop movement        
                isCollecting = False	
                agent_host.sendCommand("move 0")					
        
        #Detect nearby treestumps, and if we are not collecting items proceed to harvest the stump
        if "tree_stumps" in data and not isCollecting:
            
            #Get the observed grid
            blocks = data.get(u'tree_stumps', 0)
            index = 0
			
            #Scan the grid for treestumps
            for b in blocks:
                index += 1
                if b == u'log':               
                    # Find the correct tool in our inventory and equip it
                    neededTool = resourceToToolMapping[u'log']                 
                    if u'inventory' in data:
                        inv = [InventoryObject(**k) for k in data[u'inventory']]
                        for item in inv:
                            if item.type == neededTool:
                                itemIndex = item.index + 1
                                agent_host.sendCommand("hotbar." + str(itemIndex) + " 1")
                                agent_host.sendCommand("hotbar." + str(itemIndex) + " 0")                                                              
                
                    # Calculate the in-grid coordinates of the agent and the object
                    agent_row = 13/2
                    agent_column = agent_row
                    object_row = math.floor((index-1)/13)
                    object_column = (index-1)%float(13)
					
                    # Calculate the difference of the in-grid coordinates
                    row_diff = float(agent_row) - float(object_row)
                    column_diff = float(agent_column) - float(object_column)
					
                    #Calculate the absolute coordinate of the object
                    new_x = current_x - column_diff
                    new_z = current_z - row_diff
						
                    #Calculate the yaw needed to orientate towards the stump                
                    newYaw = calcYawToBlock(new_x, new_z, current_x, current_z)
                    deltaYaw = newYaw - yaw
                    
                    # Turn towards the stump, if we are facing it walk close enough to it for us to be able to harvest, and harvest it
                    if abs(deltaYaw) > 2:
                        while deltaYaw < -180:
                            deltaYaw += 360;
                        while deltaYaw > 180:
                            deltaYaw -= 360;
                        deltaYaw /= 90.0;
                        agent_host.sendCommand("turn " + str(deltaYaw))
                    else:
                        # Keep walking closer
                        if pathag(new_x - current_x, new_z - current_z) > 2.5:
                            agent_host.sendCommand("move 1")  
                            agent_host.sendCommand("turn 0")
                        # Stop movement to harvest the stump
                        else:
                            agent_host.sendCommand("move 0")
                            agent_host.sendCommand("turn 0")
                            if pitch < 20:
                                agent_host.sendCommand("pitch 0.5")
                            else:
                                agent_host.sendCommand("pitch 0")
                                agent_host.sendCommand("attack 1")         
                    break
					 
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission ended")
# Mission has ended.
