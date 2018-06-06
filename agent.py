from __future__ import print_function

from builtins import range
from collections import namedtuple
from tools import angles, spatial

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

# Mapping from which resources can be gathered by which tools
resourceToToolMapping = { u'log' : "iron_axe"}

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# TODO:
# Why is this here?
isCollecting = False
isDroppingOff = False

# ==============================================================================
# ========================== The Generic Agent Object ==========================
# ==============================================================================


class Agent:
# ==============================================================================
# ===================== Initializers and starting missions =====================
# ==============================================================================
    def __init__(self, missionXML):
        self.my_mission = MalmoPython.MissionSpec(missionXML,True)
        self.my_mission_record = MalmoPython.MissionRecordSpec()

        # The Malmo agent_host
        self.agent_host = MalmoPython.AgentHost()

        # Try and connect to a world
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
        
# ==============================================================================
# ================================== Wrappers ==================================
# ==============================================================================
    def SendCommand(self, command):
        """ Sends a singular command for the agent to execute """
        self.agent_host.sendCommand(command)

    def is_mission_running(self):
        """ Whether or not the agent is running """
        return self.World.is_mission_running
        
    def StopMissionManually(self):
        """ Manually stops an agents mission, useful if for some reason the XML quit conditions fail/fire too early """
        self.agent_host.sendCommand("quit")
        print("Mission ended manually")

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

# ==============================================================================
# =========================== Call these for ovement ===========================
# ==============================================================================
    def MoveToRelBLock(self, index):
        """ Move towards a block and look at it """
        self.yawd = False
        self.movd = False
        self.pitd = False

        return self.MoveLookAtBlock(spatial.LocationFromIndex(self.Position, index))

    def MoveToRelative(self, index):
        """ Move to a block at a certain index in the observable grid """
        self.yawd = False
        self.movd = False
        self.pitd = False

        return self.MoveLookAtLocation(spatial.LocationFromIndex(self.Position, index))

# ==============================================================================
# ======================== High Level Movement Commands ========================
# ==============================================================================
    def MoveLookAtBlock(self, targetLocation):
        """
            The agent moves into range of a block in the world and looks at it
            targetLocation: a tuple with (X, Y, Z) coordinates of the target area
            returns: returns a boolean whether or not the agent has arrived
        """
        targetLocationN = (targetLocation[0], targetLocation[1] + 0.5, targetLocation[2])
        return self.MoveLookAtLocation(targetLocationN, distance = 3)

    def MoveLookAtLocation(self, targetLocation, distance = 0):
        """
            The agent moves to a location in world-space
            targetLocation: a tuple with (X, Y, Z) coordinates of the target area
            returns: returns a boolean whether or not the agent has arrived
        """

        # Reset movement every step
        self.SendCommand("move 0")
        self.SendCommand("pitch 0")
        self.SendCommand("turn 0")

        # Turn towards the location in the XZ plane
        if not self.yawd:
            if self.TryTurnTo(targetLocation):
                self.yawd = True

        # Move towards it
        if self.yawd and not self.movd:
            di = spatial.dist(targetLocation[0] - self.Position[0], targetLocation[2] - self.Position[2])

            if di > distance:
                sp = min(1, di/10)
                self.agent_host.sendCommand("move "+ str(sp))
            else:
                self.movd = True

        # Turn towards the location in the XY plane
        if self.yawd and self.movd and not self.pitd:
            print(self.pitd)
            if self.TryPitchTo(targetLocation):
                self.pitd = True

        # It is there and looks at it
        if self.yawd and self.movd and self.pitd:
            return True

# ==============================================================================
# ============================ Movement Subcommands ============================
# ==============================================================================
    def TryTurnTo(self, targetLocation):
        """ Turn in the XZ plane towards the location """
        # Calculate the actual angle
        deltaYaw = angles.CalcDeltaYaw(self.Position, targetLocation)

        # If the agent's direction is within 5 degrees of the location it is fine
        if abs(deltaYaw) < 5:
            return True

        # Determine turn speed:
        sp = min(1, deltaYaw / 90)

        self.SendCommand("turn " + str(sp))
        return False

    def TryPitchTo(self, targetLocation):
        """ Makes the agent turn and look at a location """
        deltaPitch = angles.CalcDeltaPitch(self.Position, targetLocation)

        # If the agent's direction is within 5 degrees of the location it is fine
        if abs(deltaPitch) < 5:
            return True

        # Determine turn speed:
        sp = min(1, deltaPitch / 90)

        self.SendCommand("pitch " + str(sp))
        return False

# ==============================================================================
# ============================= Resource Gathering =============================
# ==============================================================================
    def EquipToolForResource(self, resource, inventory):
        """
            Looks up the needed tool for the resource to be gathered
            and equips it.
            Returns True for a succeed and False for a fail
        """
        neededTool = resourceToToolMapping[resource]

        for item in inventory:
            if item.type == neededTool:
                itemIndex = item.index + 1
                self.agent_host.sendCommand("hotbar." + str(itemIndex) + " 1")
                self.agent_host.sendCommand("hotbar." + str(itemIndex) + " 0")
                return True

        return False
