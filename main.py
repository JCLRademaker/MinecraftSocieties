from __future__ import print_function
import operator
from collections import namedtuple
from multiagent import multiserver, createMissionXML
from task import build, scout, collect, gather, handIn
import time
import tasks
import MalmoPython

# ==============================================================================
# =========================== Starting the Server ==============================
# ==============================================================================
agents = ["Jan", "Henk"]

# Parameter = force reset.
server = multiserver.MultiServer(createMissionXML.ReturnMissionXML("\"true\""))
server.StartServer(agents)

# ==============================================================================
# ========================= Implementing the Server ============================
# ==============================================================================
server.agents[1].SendMessage("Hoi", target="Jan")

while server.IsRunning():
    success, obser = server.Observe()       # Call all Agent.Observe for init
    chats = server.GetChat()                # Call all Agent.GetChat

    if success:
        for agent in server.agents:
            # Reason about a new thing to do (if returns false)
            if not agent.doCurrentTask():
                scores = server.ReasonOnPreferences()
                priority = max(scores.iteritems(), key=operator.itemgetter(1))[0]
                agent.SetPreferencesFromVote(priority)

        for i, chat in enumerate(chats):
            if chat[0]:
                for msg in chat[1]:
                    print(str(msg))

    # Give agent time to process
    time.sleep(0.3)
