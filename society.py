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

farmland = superflatWorld.MakeDrawingDecorator()
mobs = superflatWorld.ReturnMobTypes()
forceReset = "\"true\""
xml = superflatWorld.ReturnMissionXML(forceReset, farmland, mobs)

# ==============================================================================
# =========================== Initializing the Agent ===========================
# ==============================================================================

agent = Agent(xml)
agent.StartMission()
agent.addTask((tasks.returnItems, u'log'))

# ==============================================================================
# =========================== Implementing the Agent ===========================
# ==============================================================================

while agent.is_mission_running():
    success, data = agent.Observe()
    if success:
        print("running")
        # agent.doCurrentTask()

print()
print("Mission ended")
# Mission has ended.
