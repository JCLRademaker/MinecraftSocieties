def CreateAgentXML(name, coords = "", inventory = ""):
    if coords == "":
        placement = '''<Placement x="0" y="228.0" z="0" pitch="0" yaw="0"/>'''

    xml = '''<AgentSection mode="Survival">
          <Name>''' + name + '''</Name>
          <AgentStart>
                ''' + placement + '''
              <Inventory>
                ''' + inventory + '''
              </Inventory>
          </AgentStart>
          <AgentHandlers>
              <!-- observations -->
              <ObservationFromFullInventory flat="false"/>
              <ObservationFromFullStats/>
              <ObservationFromChat/>
              <ObservationFromGrid>
                  <Grid name="worldGrid" absoluteCoords="false">
                  <min x="-6" y="0" z="-6"/>
                  <max x="6" y="0" z="6"/>
                  </Grid>
              </ObservationFromGrid>

              <!-- movement -->
      	      <ContinuousMovementCommands/>
      		  <AbsoluteMovementCommands/>

              <!-- Chat -->
              <ChatCommands/>

              <!-- Inventory -->
              <InventoryCommands/>
          </AgentHandlers>
        </AgentSection>
    '''
    return xml
