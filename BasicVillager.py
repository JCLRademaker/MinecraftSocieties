from __future__ import print_function
from __future__ import division
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #5: Observations

from builtins import range
from past.utils import old_div
import MalmoPython
import os
import sys
import time
import json

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)


missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About><Summary>Hello world!</Summary></About>
            
	    <ServerSection>
              	 <ServerInitialConditions>
					<Time>
						<StartTime>1000</StartTime>
						<AllowPassageOfTime>false</AllowPassageOfTime>
					</Time>
		 </ServerInitialConditions>

               	 <ServerHandlers>
		   	<DefaultWorldGenerator/>
                  	<ServerQuitFromTimeUp timeLimitMs="0"/>
                  	<ServerQuitWhenAnyAgentFinishes/>
                 </ServerHandlers>
              </ServerSection>

 <!--****************AGENT ZONE ********************-->
              <AgentSection mode="Survival">
                <Name>BasicVillager</Name>
                <AgentStart>
                  <!--  <Placement x="0" y="0" z="90" yaw="90"/>  -->
                   
	  <!--COMMENT we can add tools but axe, shovel and others didn't work for some reason-->
		    <Inventory>
                        <InventoryItem slot="8" type="diamond_pickaxe"/>
			<InventoryItem slot="7" type="stick"/>
			<InventoryItem slot="6" type="bucket"/>
                    </Inventory>

                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ObservationFromGrid>
                      <Grid name="floor3x3">
                        <min x="-1" y="-1" z="-1"/>
                        <max x="1" y="-1" z="1"/>
                      </Grid>
                  </ObservationFromGrid>

		 <DiscreteMovementCommands />
                  <!--  <ContinuousMovementCommands turnSpeedDegs="180"/> -->

                  <InventoryCommands/>

	 <!--COMMENT apparently this is how we conclude the mission-->
                  <AgentQuitFromTouchingBlockType>
                      <Block type="diamond_block" />
                  </AgentQuitFromTouchingBlockType>

                </AgentHandlers>
              </AgentSection>
<!--****************END AGENT ZONE *********************-->
            </Mission>'''

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

my_mission = MalmoPython.MissionSpec(missionXML, True)
# my_mission.setWorldSeed("1488218954")
my_mission.setWorldSeed("-770290065")
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

#************************ AGENT COMMANDS *****************************


#agent_host.sendCommand("hotbar.9 1") #Press the hotbar key

#agent_host.sendCommand("look 1") 

agent_host.sendCommand("move ")

#agent_host.sendCommand("hotbar.9 1") #Press the hotbar key
#agent_host.sendCommand("hotbar.9 0") #Release hotbar key - agent should now be holding diamond_pickaxe
#agent_host.sendCommand("pitch 0.2") #Start looking downward slowly
#time.sleep(1)                        #Wait a second until we are looking in roughly the right direction
#agent_host.sendCommand("pitch 0")    #Stop tilting the camera
#agent_host.sendCommand("move 1")     #And start running...
#agent_host.sendCommand("attack 1")   #Whilst flailing our pickaxe!



#ok = 0

#agent_host.sendCommand("strafe 1")
#agent_host.sendCommand("strafe 1 0")

#agent_host.sendCommand("move 20")

#while ok<1000:
#	agent_host.sendCommand("move 1")     #And start running...
#	time.sleep(1) 
	 #agent_host.sendCommand("attack 1")
#	ok = ok+1

#************************ END AGENT COMMANDS **************************

jumping = False
# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)
        grid = observations.get(u'floor3x3', 0)
        if jumping and grid[4]!=u'lava':
            agent_host.sendCommand("jump 0")
            jumping = False
        if grid[3]==u'lava':
            agent_host.sendCommand("jump 1")
            jumping = True
print()
print("Mission ended")
# Mission has ended.
