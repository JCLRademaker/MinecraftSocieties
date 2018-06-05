import math

def dist(a, b):
    """ Pythagoras """
    return math.sqrt(a*a + b*b)


def LocationFromIndex(agent, index):
    # The grid is a 13x13 area, of which the agent is in the center..ish
    gridC = float(13/2)

    # In which of these rows/columns the location falls
    col = gridC - math.floor((index-1)/13)
    row = gridC - (index-1) % float(13)

    return (agent[0] - row , agent[1], agent[2] - col)
