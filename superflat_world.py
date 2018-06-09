# ------------------------------------------------------------------------------------------------ #
# ----------------------Spawns a world based on a superflat generator string---------------------- #
# ------------------------------------------------------------------------------------------------ #

from __future__ import print_function
from builtins import range
import MalmoPython
import os
import sys
import random
import time
import xml.etree.ElementTree as ET


if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools

    print = functools.partial(print, flush=True)


# Create the whole <DrawingDecorator> section here
def MakeFarmLand():
    chest_x = 2
    chest_z = 3

    crop_types = ["beetroots", "carrots", "potatoes"]
    block_type = "ender_chest"
    drawing_decorator = "<DrawingDecorator>"

    # First add the chest...
    drawing_decorator += '<DrawBlock x="' + str(chest_x) + '" y="' + str(60) + '" z="' + str(chest_z) + '"' + \
                         ' type="' + block_type + '"' + '/>'

    # ...Then create the farm plot
    for x in range(3, 8):
        for y in range(3, 8):
            if x == 5 and (y == 4 or y == 5 or y == 6):
                # Water is needed to keep the farmland hydrated (hydrates max 4 tiles around 1 water)
                block_type = "water"
                drawing_decorator += '<DrawBlock x="' + str(x) + '" y="' + str(59) + '" z="' + str(y) + '"' + \
                                     ' type="' + block_type + '"' + '/>'
            else:
                # You first need farmland
                block_type = "farmland"
                drawing_decorator += '<DrawBlock x="' + str(x) + '" y="' + str(59) + '" z="' + str(y) + '"' + \
                                     ' type="' + block_type + '"' + '/>'
                # Then you can place carrots on top of that
                block_type = crop_types[random.randint(0, len(crop_types)-1)]
                drawing_decorator += '<DrawBlock x="' + str(x) + '" y="' + str(60) + '" z="' + str(y) + '"' + \
                                     ' type="' + block_type + '"' + '/>'

    drawing_decorator += "</DrawingDecorator>"

    return drawing_decorator


# Settings
forceReset = '"true"'
d_decorator = MakeFarmLand()
mob_types = (''' Cow ''' + ''' Chicken ''' + ''' Pig ''' + ''' Rabbit ''' + ''' Sheep ''')

# Mission XML
missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <About>
                    <Summary>Hello world!</Summary>
                </About>
                <ServerSection>
                    <ServerInitialConditions>
                        <Time>
                            <StartTime>1000</StartTime>
                            <AllowPassageOfTime>false</AllowPassageOfTime>
                        </Time>
                        <Weather>clear</Weather>
                        <AllowSpawning>true</AllowSpawning>
                        <AllowedMobs>''' + mob_types + '''</AllowedMobs>
                    </ServerInitialConditions>
                    <ServerHandlers>
                        <FlatWorldGenerator generatorString="3;57*1,2*3,2;35;biome_1,decoration" forceReset=''' + forceReset + '''/>''' + d_decorator + '''
                        <ServerQuitFromTimeUp timeLimitMs="0"/>
                        <ServerQuitWhenAnyAgentFinishes/>
                    </ServerHandlers>
                </ServerSection>

                <AgentSection mode="Survival">
                    <Name>MalmoTutorialBot</Name>
                    <AgentStart>
                        <Placement x="0" y="61" z="0" pitch="0" yaw="0"/>
                        <Inventory>
                            <InventoryItem slot="0" type="diamond_pickaxe"/>
                            <InventoryItem slot="1" type="diamond_hoe"/>
                        </Inventory>
                    </AgentStart>
                    <AgentHandlers>
                        <ObservationFromFullStats/>
                        <ContinuousMovementCommands turnSpeedDegs="180"/>
                    </AgentHandlers>
                </AgentSection>
            </Mission>'''


# Create default Malmo objects:
agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print('ERROR:', e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record)
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:", e)
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
        print("Error:", error.text)

print()
print("Mission running ", end=' ')

# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:", error.text)

print()
print("Mission ended")
# Mission has ended.
