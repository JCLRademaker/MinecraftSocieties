from __future__ import print_function
import operator
from collections import namedtuple
from multiagent import multiserver, createMissionXML
from task import build, scout, collect, gather, handIn
import time
import random
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
    # chats = server.GetChat()                # Call all Agent.GetChat

    if success:
        for agent in server.agents:
            # Reason about a new thing to do (if returns false)
            if not agent.doCurrentTask():
                two_priorities = []
                scores = server.ReasonOnPreferences()

                # Tie breaking
                priority = max(scores.iteritems(), key=operator.itemgetter(1))[0]
                del scores[priority]
                priority_2 = max(scores.iteritems(), key=operator.itemgetter(1))[0]

                # Random of first two choices (prevents getting stuck gathering when adjusting thresholds)
                two_priorities.append(priority)
                two_priorities.append(priority_2)
                priority = two_priorities.__getitem__(random.randint(0, len(two_priorities)-1))

                agent.SetPreferencesFromVote(priority)

        # for i, chat in enumerate(chats):
        #     if chat[0]:
        #         for msg in chat[1]:
        #             print(str(msg))

    # Give agent time to process
    time.sleep(0.1)
