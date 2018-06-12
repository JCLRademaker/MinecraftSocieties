from __future__ import print_function
from builtins import range
from agent import Agent
import MalmoPython
import os
import sys
import time
import random
import json
import errno
import math
from collections import namedtuple
import superflatWorld
import tasks

# ==============================================================================
# =========================== Initializing the world ===========================
# ==============================================================================

farmland = superflatWorld.MakeFarmLand()
mobs = superflatWorld.ReturnMobTypes()
forceReset = "\"true\""
xml = superflatWorld.ReturnMissionXML(forceReset, farmland, mobs)

# ==============================================================================
# =========================== Initializing the Agent ===========================
# ==============================================================================

agent = Agent(xml)
agent.StartMission()

# ==============================================================================
# =========================== Implementing the Agent ===========================
# ==============================================================================

while agent.is_mission_running():
    success, data = agent.Observe()
    if success:
        if u'LineOfSight' in data:
            object, inrange = agent.getObjectFromRay(data[u'LineOfSight'])
            print(str(object) + " " +  str(inrange))
        else:
            print("nothing here")

print()
print("Mission ended")
# Mission has ended.
