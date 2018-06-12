# Defines logic to connect multiple objects of the agent class to a mission
from __future__ import print_function

from builtins import range
from collections import namedtuple
from agent import Agent

import MalmoPython
import os
import sys
import time
import json
import math

# ==============================================================================
# =========================== Initalizing the Server ===========================
# ==============================================================================

def safeStartMission(agent_host, my_mission, my_client_pool, my_mission_record, role, expId):
    used_attempts = 0
    max_attempts = 5
    print("Calling startMission for role", role)
    while True:
        try:
            # Attempt start:
            agent_host.startMission(my_mission, my_client_pool, my_mission_record, role, expId)
            break
        except MalmoPython.MissionException as e:
            errorCode = e.details.errorCode
            if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                print("Server not quite ready yet - waiting...")
                time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                print("Not enough available Minecraft instances running.")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                print("Server not found - has the mission with role 0 been started yet?")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            else:
                print("Other error:", e.message)
                print("Waiting will not help here - bailing immediately.")
                exit(1)
        if used_attempts == max_attempts:
            print("All chances used up - bailing now.")
            exit(1)
    print("startMission called okay.")

def safeWaitForStart(agent_hosts):
    print("Waiting for the mission to start", end=' ')
    start_flags = [False for a in agent_hosts]
    start_time = time.time()
    time_out = 120  # Allow a two minute timeout.
    while not all(start_flags) and time.time() - start_time < time_out:
        states = [a.peekWorldState() for a in agent_hosts]
        start_flags = [w.has_mission_begun for w in states]
        errors = [e for w in states for e in w.errors]
        if len(errors) > 0:
            print("Errors waiting for mission start:")
            for e in errors:
                print(e.text)
            print("Bailing now.")
            exit(1)
        time.sleep(0.1)
        print(".", end=' ')
    if time.time() - start_time >= time_out:
        print("Timed out while waiting for mission to start - bailing.")
        exit(1)
    print()
    print("Mission has started.")


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

    <AgentSection mode="Survival">
      <Name>Henk</Name>
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

</Mission>'''


client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )


# ==============================================================================
# =========================== Initalizing the Server ===========================
# ==============================================================================
a = Agent(xml)
a.StartMission()

b = Agent(xml)
b.StartMission()


safeStartMission(agent_host_simeon, my_mission, client_pool, simeon_recording_spec, 0, '' )
safeStartMission(agent_host_fred, my_mission, client_pool, fred_recording_spec, 1, '' )
safeWaitForStart([ agent_host_simeon, agent_host_fred ])



def MultiAgentInit():
    # Do some Python magic
    print ("done")
