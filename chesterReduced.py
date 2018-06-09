from __future__ import print_function

from agent import Agent

# ==============================================================================
# ================================ Mission Code ================================
# ==============================================================================


# Coordinates to spawn a log on.
logX = -4
logZ = -5


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
      <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" seed="" forceReset = "0"/>
      <DrawingDecorator>
		<DrawBlock x="''' + str(logX) + '''"  y="227" z="''' + str(logZ) + '''" type="ender_chest"/>
        <DrawItem x="0" y="227" z="10" type="cookie"/>
      </DrawingDecorator>
      <ServerQuitFromTimeUp description="" timeLimitMs="35000"/>
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Survival">
    <Name>Walker</Name>
    <AgentStart>
      <Placement x="0" y="227.0" z="0" pitch="0" yaw="0"/>
      <Inventory>
          <InventoryItem slot="1" type="iron_axe"/>
          <InventoryItem slot="2" type="iron_pickaxe"/>
		  <InventoryItem slot="3" type="log" quantity="63"/>
		  <InventoryItem slot="4" type="log" quantity="12"/>
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
        if "worldGrid" in data:
            # Get the observed grid
            blocks = data.get(u'worldGrid', 0)
            chestTarget = []

            index = 0

            # Scan for chests:
            for b in blocks:
                index += 1
                if b == u'ender_chest':
                    chestTarget = b
                    break

            if agent.MoveToRelBlock(index):
                agent.SendCommand("use 1")
                if u'inventoriesAvailable' in data:
                    # Adds items of a specified type to the chest
                    agent.AddItemsToChest(data[u'inventoriesAvailable'], data[u'inventory'], "enderchest", u'log')
                break

print()
print("Mission ended")
# Mission has ended.
