from collections import namedtuple
from tools import angles, spatial, inventory, crafting
from message import chat
import tasks

import movement

import MalmoPython
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

# TODO:
# Why is this here?
isCollecting = False
isDroppingOff = False


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
        # Make this nice
        self.my_mission = MalmoPython.MissionSpec(xml,True)
        self.my_mission_record = MalmoPython.MissionRecordSpec()
        self.role = role

        # Movement
        self.mov = movement.Movement(self)

        # ??????
        self.big_map = {}
        self.block_list = {}
        self.home = (25, 60, 25) #TODO: Set dynamically at spawn

        # Task queue
        self.taskList = list()
        # self.Position = (0, 61, 0, 0, 0)

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
            self.data = json.loads(msg)
            self.Position = (
                self.data.get(u'XPos', 0),
                self.data.get(u'YPos', 0),
                self.data.get(u'ZPos', 0),
                self.data.get(u'Yaw',  0),
                self.data.get(u'Pitch', 0)
            )
            return True, self.data

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
        targetLocationN = (targetLocation[0], targetLocation[1]+0.5, targetLocation[2])
        return self.mov.MoveLookAtLocation(targetLocationN, distance = 3)

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
    # ================================= Inventory ==================================
    # ==============================================================================
    def GetInventory(self, super_inventory, inventory_name):
        return inventory.GetInventory(super_inventory, inventory_name, InventoryObject)

    def GetAmountOfType(self, _inventory, item_type):
        return inventory.GetAmountOfType(_inventory, item_type)

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
    # ================================ Crafting ====================================
    # ==============================================================================
    def TryCraftItem(self, _inventory, recipe_name):
        item_crafted = False
        can_craft, craftable_elements = crafting.IsRecipeInInventory(_inventory, recipe_name)

        if can_craft and len(craftable_elements) > 0:
            for element in craftable_elements:
                self.SendCommand("craft " + str(element))
            self.SendCommand("craft " + recipe_name)
            item_crafted = True
        elif can_craft:
            self.SendCommand("craft " + recipe_name)
        else:
            missing_elements = crafting.GetMissingElements(_inventory, recipe_name)
            # return missing_elements

        if item_crafted:
            return True

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
            for j in (0, 12):
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

    # ==============================================================================
    # ============================ Vision methods ==================================
    # ==============================================================================
    """ Returns the object the agent is currently looking at and whether it is in range
        Takes the u'LineOfSight' object from the data as parameter
        Make sure that the agent has ObservationFromRay in it's agentHandlers
    """

    def getObjectFromRay(self):
        if u'LineOfSight' in self.data:
            rayObservation = self.data[u'LineOfSight']
            object = rayObservation["type"]
            inRange = rayObservation["inRange"]
            return object, inRange
        else:
            return False, False

    # ==============================================================================
    # ============================ Task execution ==================================
    # ==============================================================================

    """   Makes the given agent perform the current task from its tasklist
      Returns true when the task is done and removed from the queue
    """

    def doCurrentTask(self):
        if len(self.taskList) > 0:  # Look for tasks
            task = self.taskList[0]
            if task[0](*task[1:], agent=self):  # Perform the task and remove the task from the queue if its finished
                print(str(task[0]) + " completed.")
                del self.taskList[0]
                time.sleep(0.5)
                return True  # Task is done and removed
        return False  # Not doing a task / task is not done yet

    """
      Add a task to the agents task list
	  Tasks are in the form of (functionCall(), paramA, paramB)
    """

    def addTask(self, task):
        self.taskList.append(task)

    # ==============================================================================
    # ============================ High level task wrappers ========================
    # ==============================================================================
    """
    Adds all the subtasks for woodcutting to the agents tasklist
    """

    def addWoodcutterTask(self):
        self.addTask((tasks.moveToResource, u'log'))
        self.addTask((tasks.harvestResource, u'log'))
        self.addTask((tasks.collectResource, "log"))
        self.addTask((tasks.goToPosition, self.home))
        self.addTask((tasks.returnItems, u'log'))

    """
    Adds all the subtasks for stonecutting to the agents tasklist
    """

    def addStonecutterTask(self):
        self.addTask((tasks.moveToResource, u'stone'))
        self.addTask((tasks.harvestResource, u'stone'))
        self.addTask((tasks.collectResource, "cobblestone"))
        self.addTask((tasks.goToPosition, self.home))
        self.addTask((tasks.returnItems, u'cobblestone'))


