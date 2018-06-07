from __future__ import print_function

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
        <!-- observations -->
        <ObservationFromFullInventory flat="false"/>
        <ObservationFromFullStats/>
        <ObservationFromChat/>

        <!-- movement -->
	    <ContinuousMovementCommands/>
        <InventoryCommands/>
		<AbsoluteMovementCommands/>

        <!-- Chat -->
        <ChatCommands/>

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


agent.SendCommand("chat hoi")
agent.SendCommand("chat @hoi hey")
agent.SendCommand("chat @Walker hey")
print("Loop: \n")
while agent.is_mission_running():
    # Observe the enviroment and see everything new
    success, data = agent.Observe()
    if success:

        # Handle the chat messages
        newMsg, chat = agent.GetChat()
        if newMsg:
            for msg in chat:
                print(str(msg))

        # Continue doing your mission


print()
print("Mission ended")
# Mission has ended.
