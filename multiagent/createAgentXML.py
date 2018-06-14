def CreateAgentXML(name, coords = "", inventory = ""):
    if coords == "":
        placement = '''<Placement x="0" y="228.0" z="0" pitch="0" yaw="0"/>'''

    xml = '''<AgentSection mode="Survival">
          <Name>''' + name + '''</Name>
          <AgentStart>
            ''' + placement + '''
          </AgentStart>
          <AgentHandlers>
              <!-- observations -->
              <ObservationFromFullInventory flat="false"/>
              <ObservationFromFullStats/>
              <ObservationFromChat/>

              <!-- movement -->
      	    <ContinuousMovementCommands/>
              <InventoryCommands/>
      		<AbsoluteMovementCommands/>

              <!-- Chat -->
              <ChatCommands/>
          </AgentHandlers>
        </AgentSection>
    '''
    return xml
