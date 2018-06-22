from __future__ import print_function

from builtins import range
from agent import Agent
from random import randint, choice

import superflatWorld
import MalmoPython
import os
import sys
import time
import random
import json
import errno
import math



from collections import namedtuple

# Named tuple consisting of info on entities
EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')

# Create a named tuple type for the inventory contents.
InventoryObject = namedtuple('InventoryObject', 'type, colour, variant, quantity, inventory, index')
InventoryObject.__new__.__defaults__ = ("", "", "", 0, "", 0)


def dist(coordinatesA, coordinatesB):
    # Manhattan distance, ignoring height.
    # Input: 2 (X,Y,Z) coordinate sets
    # Returns float distance.
    return abs(coordinatesA[0] - coordinatesB[0]) + abs(coordinatesA[2] - coordinatesB[2])


# Coordinates to randomly spawn a tree on
# -- set up the mission --

xml = superflatWorld.ReturnMissionXML("\"true\"")

# ==============================================================================
# =========================== Initializing the Agent ===========================
# ==============================================================================

agent = Agent(xml)
agent.StartMission()

target_reached = True
counter = 0

# ==============================================================================
# =========================== Implementing the Agent ===========================
# ==============================================================================
# Loop until mission ends:

while agent.is_mission_running:
    success, data = agent.Observe()
    if success:
        # General purpose map update part:
        if "worldGrid" in data:
            blocks = data.get(u'worldGrid', 0)
            agent.UpdateMapEfficient(blocks)
            counter+=1
            if counter == 1:
                agent.UpdateMapFull(blocks)
                target = (0, 63, 0) # TODO: Make equal to agent starting position


        #Select a scouting destination, then move there:
        radius = 10
        min_score = 10**5
        while target_reached:
            old_target = target
            for i in range(int(radius/2)):
                x = randint(-radius, radius)
                z = choice([1,- 1])*(radius - abs(x))
                check_coordinates = (old_target[0] + x, old_target[1], old_target[2] + z)
                if not agent.CheckMap(check_coordinates):
                    score = dist(check_coordinates, agent.home)
                    if score < min_score:
                        target = check_coordinates
                        min_score = score
                        target_reached = False
            radius += 6
        agent.MoveLookAtBlock(target)
        if dist(agent.Position, target) < 6:
            target_reached = True
            # for map_key in agent.big_map:
            #     print("New small map", map_key)
            #     for row in agent.big_map[map_key]:
            #         print(row)
    #if target and agent.MoveLookAtBlock(target):
    #    target = False


    # Debugging code pls ignore
    if counter % 100 == 5:
        print("Map update {}!".format(str(counter // 100)))
        for block in agent.block_list:
            print(block)







print()
print("Mission ended")
# Mission has ended.
