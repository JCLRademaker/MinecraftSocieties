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

def ReturnMobTypes():
    mobs = (''' Cow ''' + ''' Chicken ''' + ''' Pig ''' + ''' Rabbit ''' + ''' Sheep ''')
    return mobs

# Mission XML
def ReturnMissionXML(forceReset, d_decorator, mob_types):
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
                        <ServerQuitFromTimeUp timeLimitMs="100000"/>
                        <ServerQuitWhenAnyAgentFinishes/>
                    </ServerHandlers>
                </ServerSection>

                <AgentSection mode="Survival">
                    <Name>Adam</Name>
                    <AgentStart>
                        <Placement x="0" y="61" z="0" pitch="0" yaw="0"/>
                        <Inventory>
                            <InventoryItem slot="0" type="diamond_pickaxe"/>
                            <InventoryItem slot="1" type="diamond_hoe"/>
                            <InventoryItem slot="2" type="iron_axe"/>
                            <InventoryItem slot="4" type="log" quantity="12"/>
                        </Inventory>
                    </AgentStart>
                    <AgentHandlers>
                        <ObservationFromFullInventory flat="false"/>
                        <ObservationFromRay/>
                        <InventoryCommands/>
	                 	<AbsoluteMovementCommands/>                    
                        <ObservationFromFullStats/>
                        <ContinuousMovementCommands turnSpeedDegs="180"/>
	                   	<ObservationFromNearbyEntities>
		                    <Range name="close_entities" xrange="10" yrange="3" zrange="10" update_frequency="20" />
                        </ObservationFromNearbyEntities>
                        <ObservationFromGrid>
                            <Grid name="worldGrid" absoluteCoords="false">
                            <min x="-6" y="0" z="-6"/>
                            <max x="6" y="0" z="6"/>
                            </Grid>
                        </ObservationFromGrid>
                    </AgentHandlers>
                </AgentSection>
            </Mission>'''
    return missionXML