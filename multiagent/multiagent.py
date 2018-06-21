from builtins import range
from collections import namedtuple
from tools import angles, spatial, inventory
from message import chat

import movement

import MalmoPython
import os
import sys
import time
import json
import math
# malmoutils.fix_print()
# Named tuple consisting of info on entities
EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')

# Create a named tuple type for the inventory contents.
InventoryObject = namedtuple('InventoryObject', 'type, colour, variant, quantity, inventory, index')
InventoryObject.__new__.__defaults__ = ("", "", "", 0, "", 0)

# Mapping from which resources can be gathered by which tools
resourceToToolMapping = { u'log' : "iron_axe"}


# ==============================================================================
# ========================== The Generic Agent Object ==========================
# ==============================================================================

class MultiAgent:
    def __init__(self, name, xml, role):
        self.name = name
        self.expId = ''

        # The Malmo host
        self.host = MalmoPython.AgentHost()

        # Wrappers; makes it easier to use these
        self.world_state = None

        # Chat
        self.chatter = chat.ChatClient(name)

        # TODO:
        # MAke htis niec
        self.my_mission = MalmoPython.MissionSpec(xml,True)
        self.my_mission_record = MalmoPython.MissionRecordSpec()
        self.role = role

        # Movement
        self.mov = movement.Movement(self)

        # ??????
        self.big_map = {}
        self.block_list = {}
        self.home = (25,60,25) #TODO: Set dynamically at spawn


    def StartMission(self, clientPool):
        """ """

        used_attempts = 0
        max_attempts = 5
        print("Calling startMission for role", self.role)
        while True:
            try:
                # Attempt start:
                self.host.startMission(self.my_mission, clientPool, self.my_mission_record, self.role, self.expId)
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

# ==============================================================================
# ================================== Wrappers ==================================
# ==============================================================================
    def peekWorldState(self):
        """ Peeks into the world state of the agent """
        return self.host.peekWorldState()

    def SendCommand(self, command):
        """ Sends a singular command for the agent to execute """
        self.host.sendCommand(command)

    def is_mission_running(self):
        """ Whether or not the agent is running """
        return self.world_state.is_mission_running

    def Stop(self):
        """ Manually stops an agents mission, useful if for some reason the XML quit conditions fail/fire too early """
        self.host.sendCommand("quit")
        print("Mission ended manually")

    def Observe(self):
        """ Returns whether or not the agent observed something new and the data """
        self.world_state = self.host.getWorldState()

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
        msg = self.chatter.StageMessage(message, alert = alert, target = target)
        self.SendCommand("chat " + msg)

    def GetAgentHost(self):
        """ Returns the Malmo.AgentHost """
        return self.host

# ==============================================================================
# ======================== Call these functions to Move ========================
# ==============================================================================
    def MoveToRelBlock(self, index):
        """ Move towards a block and look at it """
        return self.MoveLookAtBlock(spatial.LocationFromIndex(self.Position, index))

    def MoveToRelative(self, index):
        """ Move to a block at a certain index in the observable grid """
        return self.mov.MoveLookAtLocation(spatial.LocationFromIndex(self.Position, index))

    def LookAtBlock(self, location):
        """ """
        locN = (location[0]+0.5, location[1]+0.5, location[2]+0.5)
        return self.mov.LookAtLocation(locN)

    def LookAtRelBlock(self, index):
        """ """
        location = spatial.LocationFromIndex(self.Position, index)
        return self.LookAtBlock(location)

    def LookAtRelative(self, index):
        """ """
        location = spatial.LocationFromIndex(self.Position, index)
        return self.mov.LookAtLocation(location)

    def LookAtLocation(self, location):
        """ """
        return self.mov.LookAtLocation(location)

    def MoveLookAtBlock(self, targetLocation):
        """
            The agent moves into range of a block in the world and looks at it
            targetLocation: a tuple with (X, Y, Z) coordinates of the target area
            returns: returns a boolean whether or not the agent has arrived
        """
        targetLocationN = (targetLocation[0], targetLocation[1]-1, targetLocation[2])
        return self.mov.MoveLookAtLocation(targetLocationN, distance = 1)



    def PlaceBlock(self, targetLocation):
        # Makes the agent look to the middle of the block
        if self.Position[0] - targetLocation[0] > 0:
            dx = -0.3
        else: dx = 0.3
        if self.Position[2] - targetLocation[2] > 0:
            dz = - 0.3
        else: dz = 0.3

        loc = (targetLocation[0]+dx, targetLocation[1], targetLocation[2]+dz)

        self.mov.yawd = False
        self.mov.pitd = False

        if self.LookAtLocation(loc):
            self.SendCommand("use 1")
            self.SendCommand("use 0")
            print(loc)
            return True

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
                self.host.sendCommand("hotbar." + str(itemIndex) + " 1")
                self.host.sendCommand("hotbar." + str(itemIndex) + " 0")
                return True

        return False

# ==============================================================================
# ============================ Adding to Inventory =============================
# ==============================================================================
    def AddItemsToChest(self, available_inventories, super_inventory, other_inv_name, item_type):
        agent_inv = inventory.GetInventory(super_inventory, "inventory", InventoryObject)
        other_inv = inventory.GetInventory(super_inventory, other_inv_name, InventoryObject)

        # Only do this if the inventory is not full
        if not inventory.IsInventoryFull(other_inv):
            # Retrieve items of type [ ] from the inventory
            item_slots = inventory.GetItemsFromInventory(agent_inv, item_type)

            # Size can only be retrieved through the available inventories entry, which sucks.
            other_inv_size = inventory.GetInventorySize(available_inventories, other_inv_name)

            # Items of type [ ] in both inventory and chest
            if len(other_inv) > 0 and len(item_slots) >= 0:
                # First combine if that's possible
                item_slots = self.CombineSlots(other_inv, other_inv_name, item_slots)

                # Try and SWAP slots if there are still items left in the inventory
                if len(item_slots) > 0:
                    indices_used = inventory.FindSlotsInUse(other_inv, other_inv_name)
                    for slot in item_slots:
                        self.CombineSwapSlots(indices_used, other_inv_name, other_inv_size, slot[0])
            #  The chest is empty, add the items to the first (couple of) slot(s)
            elif len(item_slots) > 0:
                indices_used = []
                for item in item_slots:
                    self.CombineSwapSlots(indices_used, other_inv_name, other_inv_size, item[0])

    def CombineSlots(self, other_inv, other_inv_name, item_slots):
        # If there are slots left to COMBINE...
        for slot in item_slots:
            quantity_left = slot[1]
            for item in other_inv:
                if quantity_left > 0:
                    # Always update the amount of items that is left (sadly has to be done manually, skeere tijden)
                    command, quantity_left = inventory.CombineSlotsWithAgent(slot[0], other_inv_name, item, slot[1])
                    if command != "":
                        self.SendCommand(command)
                else:
                    slot = (-1, -1)
        return [x for x in item_slots if x != (-1, -1)]

    def CombineSwapSlots(self, indices_used, other_inv_name, other_inv_size, index):
        # First try and combine with the last chest slot (could be that only
        # 12 objects were added to the slot, and you want to fill that up first)
        command = inventory.CombineSlotWithAgent(index, len(indices_used) - 1, other_inv_name)
        self.SendCommand(command)

        # Update the indices that are in use by the chest (sadly has to be done manually, skeere tijden).
        command, indices_used = inventory.SwapSlotsWithAgent(index, other_inv_name, other_inv_size, indices_used)

        # Swap item from inventory with (empty) item from chest
        if command != "":
            self.SendCommand(command)

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
                block_position = (math.floor(self.Position[0]) - 6 + j, math.floor(self.Position[2])- 6 + i)
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
