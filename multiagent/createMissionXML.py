import createAgentXML
import random


def MakeDrawingDecorator():
    # Chest is always hardcoded.
    chest_x = 3
    chest_z = 4

    block_type = "sand"
    drawing_decorator = "<DrawingDecorator>"
    # Place sand to avoid cluttering of spawning area with e.g. trees/grass.
    drawing_decorator += '<DrawCuboid x1="' + str(-20) + '" y1="' + str(59) + '" z1="' + str(-10) + \
                         '" x2="' + str(20) + '" y2="' + str(59) + '" z2="' + str(20) + '"' + ' type="' + block_type + \
                         '"' + '/>'
    # Gonna gather watermelones
    block_type = "melon_block"
    for x in range(-100, 100):
        for z in range(-100, 100):
            if random.uniform(0, 1) <= 0.001:
                drawing_decorator += '<DrawBlock x="' + str(x) + '" y="' + str(60) + '" z="' + str(z) + '"' + \
                                     ' type="' + block_type + '"' + '/>'
    # Clear the spawning area.
    block_type = "air"
    drawing_decorator += '<DrawCuboid x1="' + str(-20) + '" y1="' + str(60) + '" z1="' + str(-10) + \
                         '" x2="' + str(20) + '" y2="' + str(70) + '" z2="' + str(20) + '"' + ' type="' + block_type + \
                         '"' + '/>'
    # Mountain.
    block_type = "cobblestone"
    drawing_decorator += '<DrawSphere x="' + str(-50) + '" y="' + str(60) + '" z="' + str(50) + \
                         '" radius="' + str(20) + '"' + ' type="' + block_type + '"' + '/>'
    # Chest.
    block_type = "chest"
    drawing_decorator += '<DrawBlock x="' + str(chest_x) + '" y="' + str(60) + '" z="' + str(chest_z) + '"' + \
                         ' type="' + block_type + '"' + '/>'
    # ... And done!
    drawing_decorator += "</DrawingDecorator>"

    return drawing_decorator


def ReturnMobTypes():
    # All passive mobs
    mobs = (''' Bat ''' + ''' Chicken ''' + ''' Cow ''' + ''' Donkey ''' + ''' Horse ''' + ''' Mule '''
            + ''' Pig ''' + ''' Rabbit ''' + ''' Sheep ''' + ''' Llama ''' + ''' Wolf ''')
    return mobs


# Mission XML
def ReturnMissionXML(forceReset):
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <About>
        <Summary/>
      </About>
      <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
                <AllowSpawning>true</AllowSpawning>
                <AllowedMobs>''' + ReturnMobTypes() + '''</AllowedMobs>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;57*1,2*3,2;6;biome_1,decoration" forceReset=''' + forceReset + '''/>''' + MakeDrawingDecorator() + '''
                <ServerQuitWhenAnyAgentFinishes/>
            </ServerHandlers>
        </ServerSection>''' + createAgentXML.CreateAgentXML("Jan", '''<Placement x="0" y="61" z="0" pitch="0" yaw="0"/>''') + createAgentXML.CreateAgentXML("Henk", '''<Placement x="2" y="61" z="0" pitch="0" yaw="0"/>''') + '''
    </Mission>'''
    return xml