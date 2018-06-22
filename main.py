from __future__ import print_function
from collections import namedtuple
from multiagent import multiserver, createMissionXML
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
# server.agents[1].SendMessage("Hoi", target="Jan")

while server.IsRunning():
    success, obser = server.Observe()       # Call all Agent.Observe for init
    prefScores = server.ReasonOnPreferences()     # Call all Agent.Preferences (for voting)
    chats = server.GetChat()                # Call all Agent.GetChat

    if success:
        print(prefScores)
        for i, score in enumerate(prefScores):
            pass

        for i, chat in enumerate(chats):
            if chat[0]:
                for msg in chat[1]:
                    print(str(msg))

    # Give agent time to process
    time.sleep(0.2)
