from __future__ import print_function

from multiagent import MultiAgent

import MalmoPython
import malmoutils

import time


class MultiServer:
    def __init__(self, xml):
        self.agents = []
        self.clientPool = MalmoPython.ClientPool()
        self.missionXML = xml

    def StartServer(self, names, ip = '127.0.0.1'):
        """
            Initiates a server given a certain XML file and a list of names of the agents
        """
        for i, name in enumerate(names):
            n = 10000 + i
            self.clientPool.add( MalmoPython.ClientInfo(ip, n) )

            self.agents.append( MultiAgent(name, self.missionXML, i) )

        malmoutils.parse_command_line(self.agents[0].host)

        for a in self.agents:
            a.StartMission(self.clientPool)

        self.safeWaitForStart(self.agents)

    def safeWaitForStart(self, agent_hosts):
        """
            .Helper function to make all agents wait with starting their mission,
              until all agents are ready
        """
        print("Waiting for the mission to start", end=' ')
        start_flags = [False for a in agent_hosts]
        start_time = time.time()
        time_out = 120  # Allow a two minute timeout.
        while not all(start_flags) and time.time() - start_time < time_out:
            states = [a.peekWorldState() for a in agent_hosts]
            start_flags = [w.has_mission_begun for w in states]
            errors = [e for w in states for e in w.errors]
            if len(errors) > 0:
                print("Errors waiting for mission start:")
                for e in errors:
                    print(e.text)
                print("Bailing now.")
                exit(1)
            time.sleep(0.1)
            print(".", end=' ')
        if time.time() - start_time >= time_out:
            print("Timed out while waiting for mission to start - bailing.")
            exit(1)

        # Set initial world things - the initial agent will just poison everyone
        agent_hosts[0].SendCommand('chat /gamemode survival')
        agent_hosts[0].SendCommand('chat /effect @a minecraft:hunger 4 200')

        print()
        print("Mission has started.")


# ==============================================================================
# ==================== Wrapper functions to call all agents ====================
# ==============================================================================
    def IsRunning(self):
        """
            Shows whether or not all agents are running
            returns: boolean
        """
        return all(agent.is_mission_running for agent in self.agents)

    def Observe(self):
        """
            Calls the observe function for each agent.
            returns: returns a list of tuples (succes, data)
        """
        res = []
        for a in self.agents:
            res.append(a.Observe())

        return res

    def ObservePreferences(self):
        """
            Calls the observe function for each agent.
            returns: returns a list of tuples (succes, data)
        """
        res = []
        for a in self.agents:
            res.append(a.GetPreferences())

        return res

    def GetChat(self):
        """
            Calls the GetChat function for each agent.
            returns: returns a list of tuples (succes, chatMessages)
        """
        res = []
        for a in self.agents:
            res.append(a.GetChat())

        return res
