from __future__ import print_function
from __future__ import division

from builtins import range
from builtins import object
from past.utils import old_div
import MalmoPython
import os
import random
import sys
import time
import json
import copy
import errno
import math
import xml.etree.ElementTree
import malmoutils

malmoutils.fix_print()

agent_host = MalmoPython.AgentHost()
malmoutils.parse_command_line(agent_host)
TESTING = agent_host.receivedArgument("test")

recordingsDirectory = malmoutils.get_recordings_directory(agent_host)

video_requirements = '<VideoProducer><Width>860</Width><Height>480</Height></VideoProducer>' if agent_host.receivedArgument("record_video") else ''

# dimensions of the test structure (works best with 3x3)
SIZE_X = 3
SIZE_Z = 3

# pallettes for the structure etc
pallette = ["log", "air", "mycelium","glowstone","netherrack","slime"]

def getMissionXML():
    # Draw a structure directly in front of the player.
    xpos = 0
    zpos = 0
    xorg = xpos - int(old_div(SIZE_X, 2))
    yorg = 1
    zorg = zpos + 1
    startpos = ()
    return '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <About>
        <Summary>Test build battles</Summary>
    </About>
    <ServerSection>
        <ServerHandlers>
       <FlatWorldGenerator generatorString="3;168:1;8;" forceReset="true"/>
            <ServerQuitWhenAnyAgentFinishes />
            <ServerQuitFromTimeUp timeLimitMs="25000" description="Ran out of time."/>
        </ServerHandlers>
    </ServerSection>
    <AgentSection mode="Survival">
        <Name>Han van Meegeren</Name>
        <AgentStart>
            <Inventory>
          <InventoryItem slot="1" type="iron_axe"/>
          <InventoryItem slot="2" type="iron_pickaxe"/>
          <InventoryItem slot="0" type="log" quantity="64"/>
      </Inventory>
            <Placement x="''' + str(xpos + 0.5) + '''" y="1.0" z="''' + str(zpos + 0.5) + '''"/>
        </AgentStart>
        <AgentHandlers>
            <ContinuousMovementCommands />
            <DiscreteMovementCommands />
            <InventoryCommands />
            <ObservationFromFullStats/>
            <ObservationFromRay/>
            <ObservationFromHotBar/>''' + video_requirements + '''
            </AgentHandlers>
    </AgentSection>

  </Mission>'''

class CopyAgent(object):
    ''' An agent that can sweep an area, build up a model of what blocks exist, and then copy that
    model to a new location.'''
    sentinel=(-1,-1)
    class Modes(object):
        InitSweep, InitCopy, Copy, InitSecondLevel, SecondLevel, Wait = list(range(6))

    def findHotKeyForBlockType(self, ob, type):
        '''Hunt in the inventory hotbar observations for the slot which contains the requested type.'''
        for i in range(0, 9):
            slot_name = u'Hotbar_' + str(i) + '_item'
            slot_contents = ob.get(slot_name, "")
            if slot_contents == type:
                return i+1  # +1 to convert from 0-based inventory slot to 1-based hotbar key.
        return -1

    def angvel(self, target, current, scale):
        '''Use sigmoid function to choose a delta that will help smoothly steer from current angle to target angle.'''
        delta = target - current
        while delta < -180:
            delta += 360;
        while delta > 180:
            delta -= 360;
        return (old_div(2.0, (1.0 + math.exp(old_div(-delta,scale))))) - 1.0

    def pointTo(self, ah, ob, target_pitch, target_yaw, threshold):
        '''Steer towards the target pitch/yaw, return True when within the given tolerance threshold.'''
        pitch = ob.get(u'Pitch', 0)
        yaw = ob.get(u'Yaw', 0)
        delta_yaw = self.angvel(target_yaw, yaw, 20.0)
        delta_pitch = self.angvel(target_pitch, pitch, 30.0)
        agent_host.sendCommand("turn " + str(delta_yaw))    
        agent_host.sendCommand("pitch " + str(delta_pitch))
        if abs(pitch-target_pitch) + abs(yaw-target_yaw) < threshold:
            agent_host.sendCommand("turn 0")
            agent_host.sendCommand("pitch 0")
            return True
        return False

    def __init__(self, size_x, size_z):
        self.size_x = size_x
        self.size_z = size_z
        self.mode = CopyAgent.Modes.InitSweep
        self.createTargets()
        self.createTargets2()

    def reset(self):
        self.mode = CopyAgent.Modes.InitSweep

    def createTargets(self):
        ''' Calculate yaw and pitch pairs for each block in the source and dest grids.'''
        self.targets = []
        # Source grid:
        height = 0.625  # Height from top of block (player's eyes are positioned at height of 1.625 blocks from the ground.)
        direction = 1.0
        for z in range(self.size_z, 0, -1):
            for x in range(-(old_div(self.size_x,2)),(old_div(self.size_x,2))+1):
                yaw = direction * x * math.atan(old_div(1.0,z)) * 180.0/math.pi
                distance = math.sqrt(x*x + z*z)
                pitch = math.atan(old_div(height,distance)) * 180.0/math.pi
                self.targets.append((pitch,yaw))
            direction *= -1.0

#        if TESTING:
#            # For added security in test scenario, loop backwards through targets.
#            tmp = list(self.targets)
#            tmp.reverse()
#            self.targets += tmp

        self.targets.append((0,0))
        self.targets.append(CopyAgent.sentinel)

        # Dest grid:
        height = 1.625  # Height from ground.
        direction = 1.0
        for z in range(self.size_z, 0, -1):
            for x in range(-(old_div(self.size_x,2)),(old_div(self.size_x,2))+1):
                yaw = direction * x * math.atan(old_div(1.0,z)) * 180.0/math.pi
                distance = math.sqrt(x*x + z*z)
                pitch = math.atan(old_div(height,distance)) * 180.0/math.pi
                self.targets.append((pitch,yaw))
            direction *= -1.0

        self.targets.append((0,0))


    def createTargets2(self):
        print("in targets2")
        ''' Calculate yaw and pitch pairs for each block in the source and dest grids.'''
        self.targets2 = []
        # Source grid:
        height = -0.225  # Height from top of block (player's eyes are positioned at height of 1.625 blocks from the ground.)
        direction = 1.0
        for z in range(self.size_z, 0, -1):
            for x in range(-(old_div(self.size_x,2)),(old_div(self.size_x,2))+1):
                yaw = direction * x * math.atan(old_div(1.0,z)) * 180.0/math.pi
                distance = math.sqrt(x*x + z*z)
                pitch = math.atan(old_div(height,distance)) * 180.0/math.pi
                self.targets2.append((pitch,yaw))
            direction *= -1.0

#        if TESTING:
#            # For added security in test scenario, loop backwards through targets.
#            tmp = list(self.targets2)
#            tmp.reverse()
#            self.targets2 += tmp

        self.targets2.append((0,0))
        self.targets2.append(CopyAgent.sentinel)

        # Dest grid:
        height = 0.625 # Height from ground.
        direction = 1.0
        for z in range(self.size_z, 0, -1):
            for x in range(-(old_div(self.size_x,2)),(old_div(self.size_x,2))+1):
                yaw = direction * x * math.atan(old_div(1.0,z)) * 180.0/math.pi
                distance = math.sqrt(x*x + z*z)
                pitch = math.atan(old_div(height,distance)) * 180.0/math.pi
                self.targets2.append((pitch,yaw))
            direction *= -1.0

        #self.targets2.append((0,0))

#===================================================================
#here we define the desired structure
    def init_scan(self, ah, ob):
        self.current_target = 11
        self.world = {u'log',u'log',u'log',u'log',u'log',u'log',u'log', u'log'}
        self.replay_mask = [1, 1, 1, 1, -1, 1, 1, -1, 1, 1]
        self.current_target2 = 11
        self.world2 = {u'log',u'log',u'log',u'log',u'log',u'log',u'log', u'log'}
        self.replay_mask2 = [1, 1, 1, 1, -1, 1, 1, -1, 1, 1]
        return True

#====================================================================


    def init_copy(self, ah, ob):
        self.current_replay_target = 0
        self.replay_accuracy = 0.5
        self.current_hotbar_key = -1
        return True

    def copy(self, ah, ob):
        '''Sweep the cells in the destination grid, and place blocks at the relevant positions,
        using the data we gathered in the scan phase.'''
        target_pitch, target_yaw = self.targets[self.current_target]
        hotkey = self.replay_mask[self.current_replay_target]
        if hotkey >= 0 and hotkey != self.current_hotbar_key:
            # Hotbar slot has changed - select the correct slot:
            self.current_hotbar_key = hotkey
            agent_host.sendCommand("hotbar." + str(hotkey) + " 1")  # press
            agent_host.sendCommand("hotbar." + str(hotkey) + " 0")  # release

        #sproceed = True if hotkey < 0 else False # Skip this position if there's nothing to place there.
        if hotkey < 0:
           proceed = True
        else:
           proceed = False

        if not proceed and self.pointTo(ah, ob, target_pitch, target_yaw, self.replay_accuracy):
#            if TESTING:
#                self.replay_accuracy = 1
#            else:
#                self.replay_accuracy = 5    # Once we've honed in on the first point, we can be less accurate with the rest.
            
          #s  if u'LineOfSight' in ob:
                print("proceed")
                ah.sendCommand("use")
                time.sleep(0.2)
                proceed = True
        if proceed:
            self.current_target += 1
            self.current_replay_target += 1
            print(self.current_target)
            print(len(self.targets))
            if self.current_target >= len(self.targets):
                self.current_target = 0
                return True
        return False

    def init_secondLevel(self, ah, ob):
        print("second level here")
        self.current_replay_target2 = 0
        self.replay_accuracy2 = 0.5
        self.current_hotbar_key = -1
        return True

    def secondLevel(self, ah, ob):
        print("in 2 level")
        target_pitch, target_yaw = self.targets2[self.current_target2]
        hotkey = self.replay_mask2[self.current_replay_target2]
        if hotkey >= 0 and hotkey != self.current_hotbar_key:
            # Hotbar slot has changed - select the correct slot:
            self.current_hotbar_key = hotkey
            agent_host.sendCommand("hotbar." + str(hotkey) + " 1")  # press
            agent_host.sendCommand("hotbar." + str(hotkey) + " 0")  # release
            
        if hotkey < 0:
           proceed = True
        else:
           proceed = False

        if not proceed and self.pointTo(ah, ob, target_pitch, target_yaw, self.replay_accuracy2):
#            if TESTING:
#                self.replay_accuracy = 1
#            else:
#                self.replay_accuracy = 5    # Once we've honed in on the first point, we can be less accurate with the rest.
            
          #s  if u'LineOfSight' in ob:
                print("proceed")
                ah.sendCommand("use")
                time.sleep(0.2)
                proceed = True
        if proceed:
            self.current_target2 += 1
            self.current_replay_target2 += 1
            print(self.current_target2)
            print(len(self.targets2))
            if self.current_target2 >= len(self.targets2):
                self.current_target2 = 0
                return True
        return False



#        proceed = True if hotkey < 0 else False # Skip this position if there's nothing to place there.
#        if not proceed and self.pointTo(ah, ob, target_pitch, target_yaw, self.replay_accuracy):
#            if TESTING:
#                self.replay_accuracy2 = 1
#            else:
#                self.replay_accuracy2 = 5    # Once we've honed in on the first point, we can be less accurate with the rest.
            
#            if u'LineOfSight' in ob:
#                ah.sendCommand("use")
#                proceed = True
#        if proceed:
#            self.current_target2 += 1
#            self.current_replay_target2 += 1
#            if self.current_target2 >= len(self.targets2):
#                self.current_target2 = 0
#                return True
#        return False


    def wait(self, ah, ob):
        return False    # Do nothing - only get here if we failed to complete the build.

    behaviour = {Modes.InitSweep:init_scan, Modes.InitCopy:init_copy, Modes.Copy:copy, Modes.InitSecondLevel:init_secondLevel, Modes.SecondLevel:secondLevel, Modes.Wait:wait}

    def act(self, ah, ob):
        if CopyAgent.behaviour[self.mode](self, ah, ob):
            self.mode += 1
        

# Create a bunch of build battle missions and run an agent on them.
num_iterations = 30000
if TESTING:
    num_iterations = 5

# Set up a recording
recording = False
my_mission_record = MalmoPython.MissionRecordSpec()


# Create agent to run all the missions:
agent = CopyAgent(SIZE_X, SIZE_Z)

for i in range(num_iterations):

    missionXML = getMissionXML()

    my_mission = MalmoPython.MissionSpec(missionXML, True)
    agent.reset()

    # Start the mission:
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

    print("Beginning test " + str(i) + ".")
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
    print()


    # Mission loop:
    while world_state.is_mission_running:
       
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            agent.act(agent_host, ob)
        world_state = agent_host.getWorldState()

  

    
    print()
