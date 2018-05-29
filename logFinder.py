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

EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')

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
logX = random.randint(1,10)
logZ = random.randint(1,10)

#Calculate the angle towards our target
def calcYawToMob(entity, x, y, z):
	dx = entity.x - x
	dz = entity.z - z
	yaw = -180 * math.atan2(dx, dz) / math.pi
	return yaw

  
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
      <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" seed=""/>
      <DrawingDecorator>
        <DrawItem x="''' + str(logX) + '''"  y="227" z="'''+ str(logZ) +'''" type="log"/>
        <DrawEntity x="10" y="227" z="10" type="MinecartRideable"/>
        <DrawItem x="0" y="227" z="10" type="cookie"/>
      </DrawingDecorator>
      <ServerQuitFromTimeUp description="" timeLimitMs="20000"/>
      <ServerQuitWhenAnyAgentFinishes description=""/>
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Survival">
    <Name>Walker</Name>
    <AgentStart>
      <Placement x="0" y="227.0" z="0" pitch="0" yaw="0"/>
    </AgentStart>
    <AgentHandlers>
      <ContinuousMovementCommands/>
      <ObservationFromNearbyEntities>
        <Range name="close_entities" xrange="100" yrange="20" zrange="100" update_frequency="20" />
      </ObservationFromNearbyEntities>
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
        msg = world_state.observations[-1].text
        data = json.loads(msg)
        current_x = data.get(u'XPos', 0)
        current_z = data.get(u'ZPos', 0)
        current_y = data.get(u'YPos', 0)
        yaw = data.get(u'yaw', 0)
        print("yaw = " + str(yaw))

        if "close_entities" in data:
            entities = [EntityInfo(k["x"], k["y"], k["z"], k["name"], k.get("quantity")) for k in data["close_entities"]] #Unpack the json into a tuple
            for ent in entities:
                if ent.name == "log":
					newYaw = calcYawToMob(ent, current_x, current_y, current_z)
					deltaYaw = newYaw - yaw
					if not deltaYaw == 0:
						while deltaYaw < -180:
							deltaYaw += 360;
						while deltaYaw > 180:
							deltaYaw -= 360;
						deltaYaw /= 180.0;
						# And turn:
						agent_host.sendCommand("turn " + str(deltaYaw))
						print(str(deltaYaw))
					break

    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission ended")
# Mission has ended.
