

# Put the items from the super-inventory in an InventoryObject and
# return the contents of the wanted inventory
def GetInventory(super_inventory, inventory_name, inventory_object):
    inventory = [inventory_object(**k) for k in super_inventory]
    sub_inventory = [x for x in inventory if x.inventory == inventory_name]
    # Always return a list
    if type(sub_inventory) is not list:
        sub_inventory = [sub_inventory]
    return sub_inventory


# Is the inventory fUlL??
def IsInventoryFull(inventory, inventory_size):
    if len(inventory) == 0 or len(inventory) < inventory_size:
        return False
    for item in inventory:
        if item.quantity < 64:
            return False
    return True


# Return the size of the wanted inventory (out of the available inventory pool)
def GetInventorySize(available_inventories, inventory_name):
    inv_size = -1
    for inv in available_inventories:
        if inv[u'name'] == inventory_name:
            inv_size = inv[u'size']
    return inv_size


def GetAmountOfType(inventory, item_type):
    quantity = 0
    for item in inventory:
        if item.type == item_type:
            quantity += item.quantity
    return quantity


# Retrieve item from inventory with item type (if possible)
def RetrieveItemOfType(inventory, item_type, amount_stacks=None):
    item_slots = [(x.index, x.quantity, x.type) for x in inventory if x.type == item_type]

    # Retrieve ALL if amount_stacks is NOT specified
    if amount_stacks is not None:
        total, l_select, indices = 0, list(item_slots), []
        for i in range(len(item_slots)):
            # Select the tuple with the max value
            max_slot = max(l_select, key=lambda t: t[1])
            if (total + max_slot[1]) <= amount_stacks*64:
                total += max_slot[1]
                indices.append(int(max_slot[0]))
            # Remove to allow for the next max value
            l_select.remove(max_slot)
        # Filter item_slots based on indices
        item_slots = [x for x in item_slots if x[0] in indices]

    # Always return a list
    if type(item_slots) is not list:
        item_slots = [item_slots]

    return item_slots


# Only returns the slots that are in use when triggering the function
# Malmo does not automatically update...
def FindSlotsInUse(inventory, inventory_name):
    slots_in_use = [x.index for x in inventory if x.inventory == inventory_name]
    if type(slots_in_use) is not list:
        slots_in_use = [slots_in_use]
    return slots_in_use
