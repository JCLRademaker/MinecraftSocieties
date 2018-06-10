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
import superflat_world
import tasks

# ==============================================================================
# =========================== Initializing the world ===========================
# ==============================================================================

farmland = superflat_world.MakeFarmLand()
mobs = superflat_world.ReturnMobTypes()
forceReset = "\"true\""
xml = superflat_world.ReturnMissionXML(forceReset, farmland, mobs)

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
        tasks.returnItems(u'log', data, agent)    

print()
print("Mission ended")
# Mission has ended.

