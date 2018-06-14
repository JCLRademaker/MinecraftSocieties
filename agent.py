from __future__ import print_function

from builtins import range
from collections import namedtuple
from tools import angles, spatial, inventory
from message import chat

import MalmoPython
import os
import sys
import time
import json
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

        #
        if self.agent_host.receivedArgument("help"):
            print(self.agent_host.getUsage())
            exit(0)

        # Wrappers for the Malmo framework; makes it easier to use these
        self.world_state = None

        # ??????
        self.big_map = {}
        self.block_list = {}
        self.home = (25,60,25) #TODO: Set dynamically at spawn
        self.chatter = chat.ChatClient("Walker")

    def StartMission(self):
        """ Try to connect to the server, starting the mission """
        max_retries = 3
        for retry in range(max_retries):
            try:
                self.agent_host.startMission(self.my_mission, self.my_mission_record )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:",e)
                    exit(1)
                else:
                    time.sleep(2)

        # Loop until mission starts:
        print("Waiting for the mission to start ", end=' ')

        self.world_state = self.agent_host.getWorldState()
        while not self.world_state.has_mission_begun:
            print(".", end="")
            time.sleep(0.1)
            self.world_state = self.agent_host.getWorldState()

            for error in self.world_state.errors:
                print("Error:",error.text)

        print()
        print("Mission running " + "\n", end=' ')

# ==============================================================================
# ================================== Wrappers ==================================
# ==============================================================================
    def SendCommand(self, command):
        """ Sends a singular command for the agent to execute """
        self.agent_host.sendCommand(command)

    def is_mission_running(self):
        """ Whether or not the agent is running """
        return self.world_state.is_mission_running

    def Stop(self):
        """ Manually stops an agents mission, useful if for some reason the XML quit conditions fail/fire too early """
        self.agent_host.sendCommand("quit")
        print("Mission ended manually")

    def Observe(self):
        """ Returns whether or not the agent observed something new and the data """
        self.world_state = self.agent_host.getWorldState()

        if self.world_state.number_of_observations_since_last_state > 0:
            msg = self.world_state.observations[-1].text
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

    def GetChat(self):
        """
            Returns whether or not the agent has read new chat messages
            Returns a list  of the messages in the format "<sender> message"
        """
        if self.world_state.number_of_observations_since_last_state > 0:
            msg = self.world_state.observations[-1].text
            data = json.loads(msg)
            chat = data.get(u'Chat', "")

            # Clean the chat and turn it into chat objects
            chatL = self.chatter.ReadChat(chat)
            if len(chatL) > 0:
                return True, chatL

        return False, False

    def SendMessage(self, message, alert = False, target = ""):
        """
            Sends a message in the chat
            alert: optional argument, increases the priority of the message
            target: optional argument, the name of the targeted agent
        """
        msg = self.chatter.StageMessage(message)
        self.SendCommand("chat " + msg)

# ==============================================================================
# ======================== Call these functions to Move ========================
# ==============================================================================
    def MoveToRelBlock(self, index):
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
        self.yawd = False
        self.movd = False
        self.pitd = False
        targetLocationN = (targetLocation[0], targetLocation[1] + 0.5, targetLocation[2])
        return self.MoveLookAtLocation(targetLocationN, distance = 3)

    def MoveLookAtLocation(self, targetLocation, distance = 0):
        """
            The agent moves to a location in world-space
            targetLocation: a tuple with (X, Y, Z) coordinates of the target area
            returns: returns a boolean whether or not the agent has arrived
        """

        self.yawd = False
        self.movd = False
        self.pitd = False

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
            # (self.pitd)
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

# ==============================================================================
# ================================= Inventory ==================================
# ==============================================================================
    def AddItemsToChest(self, available_inventories, super_inventory, o_inv_name, item_type, amount_stacks=None):
        agent_inv = inventory.GetInventory(super_inventory, "inventory", InventoryObject)
        o_inv = inventory.GetInventory(super_inventory, o_inv_name, InventoryObject)

        # Size can only be retrieved through the available inventories entry, which sucks.
        o_inv_size = inventory.GetInventorySize(available_inventories, o_inv_name)

        # Only do this if the inventory is not full
        if not inventory.IsInventoryFull(o_inv, o_inv_size):
            # Retrieve items of type [ ] from BOTH inventories.
            item_slots = inventory.RetrieveItemOfType(agent_inv, item_type, amount_stacks)
            o_inv_slots = inventory.RetrieveItemOfType(o_inv, item_type)

            # Items can possibly be combined with slots in chest
            if len(o_inv_slots) > 0 and len(item_slots) > 0:
                item_slots, o_inv_slots = self.CombineSlots(item_slots, o_inv_slots, o_inv_name)

                # Try and SWAP slots if there are still items left in the inventory
                item_slots = [x for x in item_slots if x[1] > 0]
                if len(item_slots) > 0:
                    indices_used = inventory.FindSlotsInUse(o_inv, o_inv_name)
                    for slot in item_slots:
                        item_slots, o_inv_slots = self.CombineSwapSlots(
                            indices_used, item_slots, o_inv_slots, o_inv_name, o_inv_size, slot)
            #  The chest is empty, add the items to the first (couple of) slot(s)
            elif len(item_slots) > 0:
                indices_used = []
                for slot in item_slots:
                    item_slots, o_inv_slots = self.CombineSwapSlots(
                        indices_used, item_slots, o_inv_slots, o_inv_name, o_inv_size, slot)

    def CombineSlots(self, item_slots, o_inv_slots, o_inv_name):
        # If there are slots left to COMBINE...
        for slot in item_slots:
            for item in o_inv_slots:
                if item[1] < 64:
                    # Update and keep track of the slots manually (sadly this has to be done because Malmo)
                    command, item_slots, o_inv_slots = inventory.CombineSlotWithAgent(
                        slot, item, item_slots, o_inv_slots, o_inv_name)
                    self.SendCommand(command)
        return item_slots, o_inv_slots

    def CombineSwapSlots(self, indices_used, item_slots, o_inv_slots, o_inv_name, o_inv_size, from_slot):
        # Try to COMBINE with the last added slot of o_inv (making sure the last slot is also stacked to 64)
        if len(indices_used) > 0:
            index = len(o_inv_slots) - 1
            if o_inv_slots[index][1] < 64:
                command, item_slots, o_inv_slots = inventory.CombineSlotWithAgent(
                    from_slot, o_inv_slots[index], item_slots, o_inv_slots, o_inv_name)
                self.SendCommand(command)
        # SWAP items with EMPTY slot(s)
        if next(x[1] for x in item_slots if x[0] == from_slot[0]) > 0:
            command, indices_used, item_slots, o_inv_slots = inventory.SwapSlotsWithAgent(
                indices_used, item_slots, o_inv_slots, o_inv_name, o_inv_size, from_slot)
            if command != "":
                self.SendCommand(command)
        return item_slots, o_inv_slots

# ==============================================================================
# ============================ Maintaining a Map ===============================
# ==============================================================================

    def UpdateMapFull(self, worldmap):
        # Input: worldmap in the form of a 13x13 worldGrid as retrieved from agent.Observe
        # Update the big_map property to reflect the observed squares
        # Update the block_list of all noteworthy blocks found.
        for i in range(13):
            for j in range(13):
                block_value = worldmap[13 * i + j]
                block_position = (math.floor(self.Position[0]) - 6 + j, math.floor(self.Position[2]) - 6 + i)
                self.UpdateMapBlock(block_value, block_position)


    def UpdateMapEfficient(self, worldmap):
        # Input: worldmap in the form of a 13x13 worldGrid as retrieved from agent.Observe
        # Update the big_map to reflect the observed squares
        # Update the block_list of all noteworthy blocks found.
        # Efficient only updates the outer rim of the observed field, rather than the entire field.
        for i in range(13):
            for j in (0,12):
                block_value = worldmap[13 * i + j]
                block_position = (math.floor(self.Position[0]) - 6 + j, math.floor(self.Position[2]) - 6 + i)
                self.UpdateMapBlock(block_value, block_position)

                block_value = worldmap[13 * j + i]
                block_position = (math.floor(self.Position[0]) - 6 + i, math.floor(self.Position[2]) - 6 + j)
                self.UpdateMapBlock(block_value, block_position)

    def UpdateMapBlock(self, block_value, block_position):
        map_key = (block_position[0] // 100, block_position[1] // 100)
        # Generate a new chunk of map if necessary
        if map_key not in self.big_map:
            self.big_map[map_key] = [[False for _ in range(100)] for _ in range(100)]

        if not self.big_map[map_key][block_position[1] % 100][block_position[0] % 100]:
            self.big_map[map_key][block_position[1] % 100][block_position[0] % 100] = block_value
            if block_value != "air":  # TODO: More filtering on non-interesting block types
                if block_value not in self.block_list:
                    self.block_list[block_value] = [block_position]
                else:
                    self.block_list[block_value].append(block_position)

    def CheckMap(self, coordinates):
        # Input: (x,y,z) coordinate tuple, of which the Y is not used.
        # Returns the type of block at that location, or False if the location has not yet been scouted.
        map_key = (coordinates[0] // 100, coordinates[2] // 100)
        return self.big_map[map_key][coordinates[2] % 100][coordinates[0] % 100]
