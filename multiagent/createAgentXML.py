def CreateAgentXML(name, coords="", inventory=""):
    xml = '''<AgentSection mode="Survival">
                     <Name>''' + name + '''</Name>
                     <AgentStart>
                         ''' + coords + '''
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
