import math


def CalcDAngle(dA, dB, maxAngle, curAngle):
    dangle = math.atan2(dA, dB) * float(180/math.pi)
    dangle -= curAngle

    while dangle < -maxAngle:
        dangle += (2 * maxAngle)
    while dangle > maxAngle:
        dangle -= (2 * maxAngle)

    return dangle


def CalcTargetPitch(agent, location):
    dx = max(abs(location[0] - agent[0]), 0.01)
    dy = max(abs(location[1] - (agent[1] + 1.5)), 0.01)

    return math.atan2(dy, dx) * float(180/math.pi)


def CalcDeltaPitch(agent, location):
    """
        Calculate the difference in pitch between the agent and the required ptich
    """

    dx = max(abs(location[0] - agent[0]), 1)
    dy = max(abs(location[1] - (agent[1] + 1.5)), 1)
    # Magic numbers: the 1.5 is the height of the face

    return CalcTargetPitch(agent, location) - agent[4]


def CalcDeltaYaw(agent, location):
    """ Calculates the difference in angle required to face a location
        returns: the angle in degrees [-180, 180]
    """
    dx = location[0] - agent[0]
    dz = location[2] - agent[2]

    dangle = math.atan2(dx, dz) * float(-180/math.pi)
    dangle -= agent[3]

    while dangle < -180:
        dangle += 360
    while dangle > 180:
        dangle -= 360

    return dangle
