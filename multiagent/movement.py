from tools import angles, spatial, inventory

# Regex fix:
# self\.[bqwertyuiopsdfghjklzxcvbnm]
# self.

class Movement:
    def __init__(self, agent):
        self.agent = agent

    def LookAtLocation(self, location, maxangle = 2):
        """ Turn and pitch towards a location in the world """

        # Reset movement every step
        self.SendCommand("move 0")
        self.SendCommand("pitch 0")
        self.SendCommand("turn 0")

        # Turn towards the location in the XZ plane
        if not self.yawd:
            if self.TryTurnTo(location, maxAngle = maxangle):
                self.yawd = True

        # Turn towards the location in the XY plane
        if self.yawd and not self.pitd:
            if self.TryPitchTo(location, maxAngle = maxangle):
                return True

    def MoveLookAtLocation(self, targetLocation, distance = 0):
        """
            The agent moves to a location in world-space
            targetLocation: a tuple with (X, Y, Z) coordinates of the target area
            returns: returns a boolean whether or not the agent has arrived
        """

        self.yawd = False
        self.movd = False
        self.pitd = False

        # Reset movement every step
        self.SendCommand("move 0")
        self.SendCommand("pitch 0")
        self.SendCommand("turn 0")

        # Turn towards the location in the XZ plane
        if not self.yawd:
            if self.TryTurnTo(targetLocation):
                self.yawd = True

        # Move towards it
        if self.yawd and not self.movd:
            di = spatial.dist(targetLocation[0] - self.agent.Position[0], targetLocation[2] - self.agent.Position[2])

            if di > distance:
                sp = min(1, di/10)
                self.SendCommand("move " + str(sp))
            else:
                self.movd = True

        # Turn towards the location in the XY plane
        if self.yawd and self.movd and not self.pitd:
            # (self.pitd)
            if self.TryPitchTo(targetLocation):
                self.pitd = True

        # It is there and looks at it
        if self.yawd and self.movd and self.pitd:
            return True

# ==============================================================================
# ============================== Helper functions ==============================
# ==============================================================================

    def peekWorldState(self):
        """ Peeks into the world state of the agent """
        return self.agent.peekWorldState()

    def SendCommand(self, command):
        """ Sends a singular command for the agent to execute """
        self.agent.SendCommand(command)

    def is_mission_running(self):
        """ Whether or not the agent is running """
        return self.agent.world_state.is_mission_running

    def TryTurnTo(self, targetLocation, maxAngle = 5):
        """ Turn in the XZ plane towards the location """
        # Calculate the actual angle
        # print(str(self.agent.Position))
        deltaYaw = angles.CalcDeltaYaw(self.agent.Position, targetLocation)

        # If the agent's direction is within maxAngle degrees of the location it is fine
        if abs(deltaYaw) < maxAngle:
            return True

        # Determine turn speed:
        sp = min(1, deltaYaw / 90)

        self.SendCommand("turn " + str(sp))
        return False

    def SetPitchTo(self, targetLocation):
        sp = angles.CalcTargetPitch(self.agent.Position, targetLocation)
        self.SendCommand("setPitch " + str(sp))
        return True


    def TryPitchTo(self, targetLocation, maxAngle = 5):
        """ Makes the agent turn and look at a location """
        deltaPitch = angles.CalcDeltaPitch(self.agent.Position, targetLocation)

        # If the agent's direction is within 5 degrees of the location it is fine
        if abs(deltaPitch) < maxAngle:
            return True

        # Determine turn speed:
        sp = min(1, deltaPitch / 90)

        self.SendCommand("pitch " + str(sp))
        return False
