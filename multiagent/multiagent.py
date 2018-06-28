from collections import namedtuple
from tools import angles, spatial, inventory, crafting
from message import chat
from task import build, scout, collect, gather, handIn, replenish
import tasks

import movement
from PIL import Image

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

# Mapping only for the function for making maps. Real convenient.
colourMapping = {"air": (128, 128, 128), "tallgrass": (128, 128, 127), "dirt": (125,128,128),
                 "double_plant": (127,128,128), "red_flower": (126,128,128), "yellow_flower": (128,127,128),
                 "vine":(129,128,128), 
                 "brown_mushroom": (1,255,0),
                 "stone": (0,0,255), "coal_ore": (166,42,42), "iron_ore": (166,41,42),
                 "log": (165, 42, 42), "log2": (164, 42, 42),
                 "chest": (255, 192, 203)}
                 

# ==============================================================================
# ========================== The Generic Agent Object ==========================
# ==============================================================================

class MultiAgent:
    def __init__(self, name, xml, role):
        self.chest_location = (3 + 0.5, 60, 4 + 0.5)
        self.chest = ()
        self.inventory = ()
        self.name = name
        self.expId = ''

        # The Malmo host
        self.host = MalmoPython.AgentHost()
        self.world_state = None
        self.data = []

        # Chat
        self.chatter = chat.ChatClient(name)

        # TODO: make this nice
        self.my_mission = MalmoPython.MissionSpec(xml,True)
        self.my_mission_record = MalmoPython.MissionRecordSpec()
        self.role = role

        # Movement
        self.mov = movement.Movement(self)

        # ??????
        self.big_map = {}
        self.block_list = {}
        self.home = (0, 61, 0)  # TODO: Set dynamically at spawn
        self.Position = (0, 61, 0, 0, 0)
        self.scoutingBlacklist = ["air", "tallgrass", "vine", "dirt", "brown_mushroom", "red_mushroom", "red_flower"]

        # Task queue - scouting is the initial task for all agents
        self.taskList = list()
        self.addTask(scout.ScoutTask(self, 20))

        # All preferences (in order) and initial preference list
        self.AllPreferences = ["build", "scout", "gather", "mine", "replenish"]
        self.Preference = ["scout", "gather", "mine", "build", "replenish"]
        # For getting the results of the Borda voting (so that a task can be pushed to the queue)
        self.priority = ""

        # Thresholds for determining preferences (can be changed, just initial numbers here)
        self.hpThreshold = 15
        self.hungerThreshold = 15
        self.mineThreshold = 14  # Processed materials like planks (so not logs)
        self.foodThreshold = 8
        self.scoutThreshold = 2

        self.melons_in_chest = 0
        self.wood_in_chest = 0

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

            self.AdjustPreferences()

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
        self.mov.yawd = False
        self.mov.pitd = False
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

    def LookAtLocation(self, location, maxAngle=5):
        """ """
        self.mov.yawd = False
        self.mov.pitd = False
        return self.mov.LookAtLocation(location, maxAngle)

    def MoveLookAtBlock(self, targetLocation):
        """
            The agent moves into range of a block in the world and looks at it
            targetLocation: a tuple with (X, Y, Z) coordinates of the target area
            returns: returns a boolean whether or not the agent has arrived
        """
        self.mov.yawd = False
        self.mov.movd = False
        self.mov.pitd = False
        targetLocationN = (targetLocation[0], targetLocation[1]+0.5, targetLocation[2])
        return self.mov.MoveLookAtLocation(targetLocationN, distance = 3)

    def LookAtopBlock(self, location):
        """ Look at the top of a block in 3D coordinates """

        # Calcualte the center of the block
        tLoc = (location[0] +  0.5, location[1] + 1, location[2] +  0.5)
        return self.LookAtLocation(tLoc, 0.3)

    def MoveToLocation(self, location, distance = 0):
        """  """
        self.mov.yawd = False
        self.mov.movd = False
        self.mov.pitd = False

        return self.mov.MoveToLocation(location, distance)

    def PlaceBlock(self, targetLocation):
        """ Looks at middle of where a block should be, then place it """


        if self.LookAtopBlock(targetLocation):
            raydat = self.data.get(u'LineOfSight',False)

            if raydat:
                if raydat[u'y'] > targetLocation[1]+1:
                    return True

            self.SendCommand("use 1")
            self.SendCommand("use 0")
            time.sleep(0.1)

        return False

# ==============================================================================
# ============================== Preferences ===================================
# ==============================================================================

    def AdjustPreferences(self):
        raydat = self.data.get(u'LineOfSight', False)
        self.Preference = []
        inv = self.GetInventory("inventory")

        # Only get chest information if you are looking at it
        if raydat and raydat[u'type'] == "chest" and raydat["inRange"]:
            self.chest = self.GetInventory("chest")
        
        # Get stats for reasoning
        hunger = int(self.data[u'Food'])
        # health = self.data[u'Life']
        cobblestones = self.GetAmountOfType(inv, "cobblestone")
        melons = self.melons_in_chest + self.GetAmountOfType(inv, "melon")
        logs = self.wood_in_chest + self.GetAmountOfType(inv, "log")
        
        # HP/Hunger
        if hunger < self.hungerThreshold:
            self.Preference.append("replenish")

        # Food gathering
        if melons < self.foodThreshold:
            self.Preference.append("gather")

        # Mining
        if logs + cobblestones < self.mineThreshold:
            self.Preference.append("mine")

        # Scouting
        if self.InformationCount() < self.scoutThreshold:
            self.Preference.append("scout")

        # Build has priority if the rest wasn't appended
        self.Preference.append("build")

        # Check if all the preference entries are in the list
        for pref in self.AllPreferences:
            if pref not in self.Preference:
                self.Preference.append(pref)

    def GetPreferences(self):
        preference = (self.name, self.Preference)
        return preference
        
    def SetPreferencesFromVote(self, _priority):
        self.priority = _priority
        resourceKBCount = 0        
        
        # Replenishing always has priority #weWantToLive
        if self.Preference[0] == "replenish":
            self.addTask(replenish.ReplenishTask(self))          
            self.SendMessage("I'm eating food")
            return

        # Add task(s) based on group priority
        if self.priority == "mine":
            if u'log' in self.block_list:
                resourceKBCount = len(self.block_list[u'log'])
            if resourceKBCount > 0:  # We know there is a resource so mine it
                self.SendMessage("I'm gathering wood")
                self.addTask(gather.GatherTask(self, u'log'))
                self.addTask(collect.CollectTask(self, "log"))
                self.addTask(handIn.HandInTask(self, u'log'))
            else:   # We need to scout for the resource
                self.SendMessage("I'm scouting")
                self.addTask(scout.ScoutTask(self, self.InformationCount()+10))
        elif self.priority == "gather":
            if u'melon_block' in self.block_list:
                resourceKBCount = len(self.block_list[u'melon_block'])
            if resourceKBCount > 0:     # We know there is a resource so mine it
                self.addTask(gather.GatherTask(self, u'melon_block'))
                self.addTask(collect.CollectTask(self, "melon"))
                self.addTask(handIn.HandInTask(self, "melon"))
                self.SendMessage("I'm gathering food")
            else: # We need to scout for the resource
                self.SendMessage("I'm scouting")
                self.addTask(scout.ScoutTask(self, self.InformationCount()+10))
        elif self.priority == "build":
            self.SendMessage("I'm building")
            self.addTask(build.BuildTask(self, (10, 61, 10)))
        else:
            self.SendMessage("I'm scouting")
            self.addTask(scout.ScoutTask(self, self.InformationCount()+10))

        for i in range(1000):
            i += 1

        self.SendCommand("setPitch 0")

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
    def GetInventory(self, inventory_name):
        return inventory.GetInventory(self.data[u'inventory'], inventory_name, InventoryObject)

    def GetAmountOfType(self, _inventory, item_type):
        return inventory.GetAmountOfType(_inventory, item_type)
       
    def GetItemFromChest(self, _inventory, item_type, stack_amount=1):
        return inventory.RetrieveItemOfType(_inventory, item_type, stack_amount)

    def AddItemsToChest(self, super_inventory, o_inv_name, item_type, amount_stacks=None):
        raydat = self.data[u'LineOfSight']

        if u'inventoriesAvailable' in self.data:
            if (raydat and raydat[u'type'] == "chest" and raydat["inRange"]) or \
                    self.MoveLookAtBlock(self.chest_location):
                # Give a little time-out
                for i in range(1000):
                    i += 1

                agent_inv = inventory.GetInventory(self.data[u'inventory'], "inventory", InventoryObject)
                o_inv = inventory.GetInventory(self.data[u'inventory'], "chest", InventoryObject)

                # Get the item slots of which items have to be moved to the chest
                item_slots = inventory.RetrieveItemOfType(agent_inv, item_type, amount_stacks)

                # Not going through the computational trouble (armor slots excluded)
                o_inv_size = 36

                # Only do this if the inventory is not full
                if not inventory.IsInventoryFull(o_inv, o_inv_size) and len(item_slots) > 0:
                    # First try to combine everything
                    for item in item_slots:
                        for x in range(o_inv_size):
                            # print("Going to combine with index: " + str(x))
                            self.SendCommand(
                                "combineInventoryItems chest" + ":" + str(x) + " inventory:" + str(item[0]))

                    # o_inv = inventory.GetInventory(self.data[u'inventory'], "chest", InventoryObject)
                    for i in range(5000):
                        i += 1

                    o_inv = inventory.GetInventory(self.data[u'inventory'], "chest", InventoryObject)
                    indices_used = inventory.FindSlotsInUse(o_inv, o_inv_name)

                    # Then try to swap
                    for item in item_slots:
                        for y in range(o_inv_size):
                            if y not in indices_used:
                                indices_used.append(y)
                                self.SendCommand(
                                    "swapInventoryItems inventory" + ":" + str(item[0]) + " chest:" + str(y))
                                break
                else:   # The chest is empty
                    i = 0
                    for item in item_slots:
                        self.SendCommand(
                            "swapInventoryItems inventory" + ":" + str(item[0]) + " chest:" + str(i))
                        i += 1

                return True
        return False

    def AddItemsToInv(self, super_inventory, chest_inv_name, item_type, amount_stacks=1):
        for i in range(1000):
            i += 1

        raydat = self.data[u'LineOfSight']

        if u'inventoriesAvailable' in self.data:
            if (raydat and raydat[u'type'] == "chest" and raydat["inRange"]) or \
                    self.MoveLookAtBlock(self.chest_location):
                chest_inv = inventory.GetInventory(super_inventory, chest_inv_name, InventoryObject)
                o_inv = inventory.GetInventory(super_inventory, "inventory", InventoryObject)

                item_slots = inventory.RetrieveItemOfType(chest_inv, item_type, amount_stacks)

                # Not going through the computational trouble.
                o_inv_size = 27

                # Only do this if the inventory is not full
                if not inventory.IsInventoryFull(o_inv, o_inv_size) and len(item_slots) > 0:
                    indices_used = inventory.FindSlotsInUse(o_inv, "inventory")

                    # If there are no items of type in inventory
                    for x in range(o_inv_size):
                        if x not in indices_used:
                            self.SendCommand(
                                "swapInventoryItems chest" + ":" + str(item_slots[0][0]) + " inventory:" + str(x))
                            break
                return True
        return False

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

        # Check which maps are needed, and load them in :
        corners = [(0,12), (12,0), (0,0), (12,12)]
        maps = {}
        for (i,j) in corners:
            block_position = (math.floor(self.Position[0]) - 6 + j, math.floor(self.Position[2]) - 6 + i)
            map_key = (block_position[0] // 100, block_position[1] // 100)
            try:
                map = Image.open("maps/map{}{}.png".format(map_key[0],map_key[1]))
            except IOError:
                map = Image.new("RGB", (100,100), "black")
            maps[map_key] = (map.load(), map)

        # Update the pixel maps with the newly found information
        for i in range(13):
            for j in range(13):
                block_value = worldmap[13 * i + j]
                block_position = (math.floor(self.Position[0]) - 6 + j, math.floor(self.Position[2]) - 6 + i)
                self.UpdateMapBlock(block_value, block_position, maps)

        # Save the used maps back to where they came from
        for map_key in maps:
            maps[map_key][1].save("map{}{}.png".format(map_key[0],map_key[1]))


    def UpdateMapEfficient(self, worldmap):
        # Input: worldmap in the form of a 13x13 worldGrid as retrieved from agent.Observe
        # Update the big_map to reflect the observed squares
        # Update the block_list of all noteworthy blocks found.
        # Efficient only updates the outer rim of the observed field, rather than the entire field.

        # Check which maps are needed, and load them in :
        corners = [(0, 12), (12, 0), (0, 0), (12, 12)]
        maps = {}
        for (i, j) in corners:
            block_position = (math.floor(self.Position[0]) - 6 + j, math.floor(self.Position[2]) - 6 + i)
            map_key = (block_position[0] // 100, block_position[1] // 100)
            try:
                map = Image.open("map{}{}.png".format(map_key[0], map_key[1]))
            except IOError:
                map = Image.new("RGB", (100, 100), "black")
            maps[map_key] = (map.load(), map)

        # Update the pixel maps with the newly found information
        for i in range(13):
            for j in (0,12):
                block_value = worldmap[13 * i + j]
                block_position = (math.floor(self.Position[0]) - 6 + j, math.floor(self.Position[2]) - 6 + i)
                self.UpdateMapBlock(block_value, block_position, maps)

                block_value = worldmap[13 * j + i]
                block_position = (math.floor(self.Position[0]) - 6 + i, math.floor(self.Position[2]) - 6 + j)
                self.UpdateMapBlock(block_value, block_position, maps)

        # Save the used maps back to where they came from
        for map_key in maps:
            maps[map_key][1].save("map{}{}.png".format(map_key[0], map_key[1]))


    def UpdateMapBlock(self, block_value, block_position, maps):
        map_key = (block_position[0] // 100, block_position[1] // 100)
        #if maps[map_key][0][block_position[1] % 100, block_position[0] % 100] == (0, 0, 0):
        try:
            maps[map_key][0][block_position[1] % 100, block_position[0] % 100] = colourMapping[block_value]
        except KeyError:
            maps[map_key][0][block_position[1] % 100, block_position[0] % 100] = (255, 255, 255)
        if block_value not in self.scoutingBlacklist:
            if block_value not in self.block_list:
                self.block_list[block_value] = [block_position]
            else:
                if block_position not in self.block_list[block_value]:
                    self.block_list[block_value].append(block_position)

    def CheckMap(self, coordinates):
        # Input: (x,y,z) coordinate tuple, of which the Y is not used.
        # Returns the type of block at that location, or False if the location has not yet been scouted.
        map_key = (coordinates[0] // 100, coordinates[2] // 100)
        try:
            map = Image.open("map{}{}.png".format(map_key[0], map_key[1]))
        except IOError:
            return False
        pixels = map.load()
        if pixels[coordinates[2] % 100,coordinates[0] % 100] == (0,0,0):
            return False
        for key in colourMapping:
            if colourMapping[key] == pixels[coordinates[2] % 100,coordinates[0] % 100]:
                return key
        return "unknown"
        
    def InformationCount(self):
        # Returns the amount of relevant information points in the agents knowledge base
        count = 0
        
        for type in self.block_list:
            count += len(self.block_list[type])
        
        return count

    # ==============================================================================
    # ============================ Vision methods ==================================
    # ==============================================================================
    def getObjectFromRay(self):
        """ Returns the object the agent is currently looking at and whether it is in range
            Takes the u'LineOfSight' object from the data as parameter
            Make sure that the agent has ObservationFromRay in it's agentHandlers
        """
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
        if len(self.taskList) > 0:  # We have a task to do
            task = self.taskList[0]
            if task.Execute(self):
                del self.taskList[0]
            return True
        # We have to find something new to do
        return False

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

    """
       Adds all the subtasks for gathering to the agents tasklist
    """
    def addGatheringTask(self):
        self.addTask((tasks.moveToResource, u'melon_block'))
        self.addTask((tasks.harvestResource, u'melon_block'))
        self.addTask((tasks.collectResource, "melon"))
        self.addTask((tasks.goToPosition, self.home))
        self.addTask((tasks.returnItems, u'melon'))
