def CreateAgentXML(name, coords = "", inventory = ""):
    if coords == "":
        placement = '''<Placement x="0" y="61" z="0" pitch="0" yaw="0"/>'''

    xml = '''<AgentSection mode="Survival">
                     <Name>''' + name + '''</Name>
                     <AgentStart>
                         ''' + placement + '''
                         <Inventory>
                             <InventoryItem slot="0" type="planks" quantity="1"/>
                             <InventoryItem slot="1" type="stick" quantity="2"/>
                             <InventoryItem slot="2" type="cobblestone" quantity="3"/>
                         </Inventory>
                     </AgentStart>
                     <AgentHandlers>
                         <ObservationFromFullInventory flat="false"/>
                         <ObservationFromRay/>
                         <InventoryCommands/>
                         <AbsoluteMovementCommands/>                    
                         <ObservationFromFullStats/>
                         <ContinuousMovementCommands turnSpeedDegs="180"/>
                         <SimpleCraftCommands/>
                         <ObservationFromNearbyEntities>
                             <Range name="close_entities" xrange="10" yrange="3" zrange="10" update_frequency="20" />
                         </ObservationFromNearbyEntities>
                         <ObservationFromGrid>
                             <Grid name="worldGrid" absoluteCoords="false">
                                 <min x="-6" y="0" z="-6"/>
                                 <max x="6" y="0" z="6"/>
                             </Grid>
                         </ObservationFromGrid>
                         <ChatCommands/>
                     </AgentHandlers>
                 </AgentSection>'''
    return xml
