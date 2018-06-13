from __future__ import print_function

from builtins import range
from collections import namedtuple
from multiagent import multiserver

import time

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

  <AgentSection mode="Survival">
    <Name>Henk</Name>
    <AgentStart>
      <Placement x="0" y="228.0" z="0" pitch="0" yaw="0"/>
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

agents = ["Walker", "Henk"]

server = multiserver.MultiServer(xml)
server.StartServer(agents)

server.agents[1].SendMessage("Hoi", target="Walker")

while server.IsRunning():
    # Handle Agent 1:
    obser = server.Observe()
    chats = server.GetChat()

    for i, obs in enumerate(obser):
        if obs[0]:
            # Handle the obeservation data
            pass

    for i, chat in enumerate(chats):
        if chat[0]:
            for msg in chat[1]:
                print(str(msg))
