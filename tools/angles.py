import math

def CalcDAngle(dA, dB, maxAngle, curAngle):
    dangle = math.atan2(dA, dB) * float(180/math.pi)
    dangle -= curAngle

    while dangle < -maxAngle:
        dangle += (2 * maxAngle)
    while dangle > maxAngle:
        dangle -= (2 * maxAngle)

    return dangle

def CalcDeltaPitch(agent, location):
    dx = max(abs(location[0] - agent[0]), 1)
    dy = max(abs(location[1] - agent[1]), 1)

    deltaPitch = CalcDAngle(dy, dx, 90, agent[4])

    return deltaPitch



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
