from __future__ import print_function

from builtins import range
from collections import namedtuple

from agent import Agent

# ==============================================================================
# ================================ Mission Code ================================
# ==============================================================================


# Coordinates to randomly spawn a tree on
logX = -4
logZ = -5

logXX = -2
logZZ = -1


# Mission XML
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
		<DrawBlock x="''' + str(logX) + '''"  y="227" z="'''+ str(logZ) +'''" type="chest"/>
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

# ==============================================================================
# =========================== Initializing the Agent ===========================
# ==============================================================================

agent = Agent(xml)
agent.StartMission()

# ==============================================================================
# =========================== Implementing the Agent ===========================
# ==============================================================================


while agent.is_mission_running():
    success, data = agent.Observe()
    if success:
        # Detect nearby treestumps, and if we are not collecting items proceed to harvest the stump
        if "worldGrid" in data:

            # Get the observed grid
            blocks = data.get(u'worldGrid', 0)
            chestTarget = []

            index = 0

            # Scan for chests:
            for b in blocks:
                index += 1
                if b == u'chest':
                    chestTarget = b
                    break

            if agent.MoveToRelative(index):
                agent.sendCommand("use 1")
                agent.sendCommand("use 0")



print()
print("Mission ended")
# Mission has ended.
