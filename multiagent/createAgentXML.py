def CreateAgentXML(name, coords = "", inventory = ""):
    if coords == "":
        placement = '''<Placement x="0" y="61" z="0" pitch="0" yaw="0"/>'''
    else:
        placement = '''<Placement x="'''+ str(coords[0])+ '''" y="'''+ str(coords[1])+ '''" z="'''+ str(coords[2])+ '''" pitch="0" yaw="0"/>'''

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
                       <ObservationFromRay/>
                       <ObservationFromFullStats/>
                       <ObservationFromNearbyEntities>
                            <Range name="close_entities" xrange="10" yrange="3" zrange="10" update_frequency="20" />
                       </ObservationFromNearbyEntities>
                       <ObservationFromGrid>
                         <Grid name="worldGrid" absoluteCoords="false">
                             <min x="-6" y="0" z="-6"/>
                             <max x="6" y="0" z="6"/>
                         </Grid>
                       </ObservationFromGrid>

                       <!-- movement -->
                       <ContinuousMovementCommands turnSpeedDegs="180"/>
                       <AbsoluteMovementCommands/>

                        <!-- Chat -->
                        <ChatCommands/>
                        <SimpleCraftCommands/>

                        <!-- Inventory -->
                        <InventoryCommands/>
                     </AgentHandlers>
                 </AgentSection>'''
    return xml
