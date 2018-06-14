import math

def dist(a, b):
    """ Pythagoras """
    return math.sqrt(a*a + b*b)


def LocationFromIndex(agent, index):
    # The grid is a 13x13 area, of which the agent is in the center..ish

    gridC = 13/2    # gridC = float(13)/2

    # In which of these rows/columns the location falls
    col = gridC - math.floor((index-1)/13)
    row = gridC - (index-1) % float(13)

    return (agent[0] - row , agent[1], agent[2] - col)

def IndexFromLocation(agent, location):
    x = location[0]
    y = location[1]
    z = location[2]

    gridC = float(13)/2

    # col: difference between -6 and the diff
    dy = location[2] - agent[2]
    col = dy + 6

    # row: difference between -6 and the diff
    dx = location[0] - agent[0]
    row = dx +6

    # Each column is worth 13 rows
    index = 13 * col + row
    return index

def IndexFromDifference(diff):
    row = diff[0] + 6
    col = (diff[2] + 6) * 13

    return row + col
