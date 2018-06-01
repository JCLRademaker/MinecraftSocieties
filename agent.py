from __future__ import print_function

from builtins import range
from collections import namedtuple

import MalmoPython
import os
import sys
import time
import random
import json
import errno
import math

# Named tuple consisting of info on entities
EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')

# Create a named tuple type for the inventory contents.
InventoryObject = namedtuple('InventoryObject', 'type, colour, variant, quantity, inventory, index')
InventoryObject.__new__.__defaults__ = ("", "", "", 0, "", 0)

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)


#Calculate the angle towards our target
def calcYawToBlock(objectx, objectz, agentx, agentz):
    dx = objectx - agentx
    dz = objectz - agentz
    yaw = -180 * math.atan2(dx, dz) / math.pi
    return yaw

#Calculate the angle towards our target
def calcYawToEntity(entity, x, y, z):
	dx = entity.x - x
	dz = entity.z - z
	yaw = -180 * math.atan2(dx, dz) / math.pi
	return yaw

def pathag(sidea, sideb):
    csquare = (sidea ** 2) + (sideb ** 2)
    sidec = math.sqrt(csquare)
    return sidec

def tryEquipItem(itemName):
    test = "ik neuk jullie allemaal de moeder"

isCollecting = False
isDroppingOff = False

def LocationFromIndex(agent, index):
    # The grid is a 13x13 area, of which the agent is in the center..ish
    gridC = float(13/2)

    # In which of these rows/columns the location falls
    col = gridC - math.floor((index-1)/13)
    row = gridC - (index-1) % float(13)

    return (agent[0] - row , agent[1], agent[2] - col)


class Agent:
    def __init__(self, missionXML):
        self.my_mission = MalmoPython.MissionSpec(missionXML,True)
        self.my_mission_record = MalmoPython.MissionRecordSpec()

        self.MissionLoop = None

        self.agent_host = MalmoPython.AgentHost()

        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:',e)
            print(self.agent_host.getUsage())
            exit(1)
        if self.agent_host.receivedArgument("help"):
            print(self.agent_host.getUsage())
            exit(0)

        self.World = None


    def StartMission(self):
        """ Try to connect to the server, starting the mission """
        max_retries = 3
        for retry in range(max_retries):
            try:
                self.agent_host.startMission( self.my_mission, self.my_mission_record )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:",e)
                    exit(1)
                else:
                    time.sleep(2)

        # Loop until mission starts:
        print("Waiting for the mission to start ", end=' ')

        self.World = self.agent_host.getWorldState()
        while not self.World.has_mission_begun:
            print(".", end="")
            time.sleep(0.1)
            self.World = self.agent_host.getWorldState()

            for error in self.World.errors:
                print("Error:",error.text)

        print()
        print("Mission running ", end=' ')

    def is_mission_running(self):
        """ Whether or not the agent is running """
        return self.World.is_mission_running

    def Observe(self):
        """ Returns whether or not the agent observed something new and the data """
        self.World = self.agent_host.getWorldState()

        if self.World.number_of_observations_since_last_state > 0:
            msg = self.World.observations[-1].text
            data = json.loads(msg)
            self.Position = (
                data.get(u'XPos', 0),
                data.get(u'YPos', 0),
                data.get(u'ZPos', 0),
                data.get(u'Yaw',  0),
                data.get(u'Pitch',0)
            )
            return True, data

        return False, False


    def MoveToLocation(self, targetLocation):
        """
            The agent moves to a location in world-space
            returns: returns a boolean whether or not the agent has arrived
        """
        #Calculate the yaw needed to orientate towards the stump
        newYaw = calcYawToBlock(targetLocation[0], targetLocation[2], self.Position[0], self.Position[2])
        deltaYaw = newYaw - self.Position[3]

        # Turn towards the stump, if we are facing it walk close enough to it for us to be able to harvest, and harvest it
        if abs(deltaYaw) > 2:
            while deltaYaw < -180:
                deltaYaw += 360;
            while deltaYaw > 180:
                deltaYaw -= 360;
            deltaYaw /= 90.0;
            self.agent_host.sendCommand("turn " + str(deltaYaw))
        else:
            # Keep walking closer
            if pathag(targetLocation[0] - self.Position[0], targetLocation[2] - self.Position[2]) > 2.5:
                self.agent_host.sendCommand("move 1")
                self.agent_host.sendCommand("turn 0")
            # Stop movement to harvest the stump
            else:
                self.agent_host.sendCommand("move 0")
                self.agent_host.sendCommand("turn 0")
                if self.Position[4] < 20:
                    self.agent_host.sendCommand("pitch 0.5")
                else:
                    self.agent_host.sendCommand("pitch 0")
                    return True

    def MoveToRelative(self, index):
        """ Mobseove to a block at a certain index in the observable grid """
        # Calculate the in-grid coordinates of the agent and the object
        agent_row = 13/2
        agent_column = agent_row
        object_row = math.floor((index-1)/13)
        object_column = (index-1)%float(13)

        # Calculate the difference of the in-grid coordinates
        row_diff = float(agent_row) - float(object_row)
        column_diff = float(agent_column) - float(object_column)

        # Hereafter we have x and z coordinates

        #Calculate the absolute coordinate of the object
        new_x = self.Position[0] - column_diff
        new_z = self.Position[2] - row_diff

        return self.MoveToLocation((new_x, self.Position[1], new_z))


    def SendCommand(self, command):
        """ Sends a singular command for the agent to execute """
        self.agent_host.sendCommand(command)
