

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


# Retrieve item from inventory with item type (if possible)
def RetrieveItemOfType(inventory, item_type, amount_stacks=None):
    item_slots = [(x.index, x.quantity) for x in inventory if x.type == item_type]

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


# Use Malmo's combine option if it's possible
def CombineSlotWithAgent(from_slot, to_slot, item_slots, o_inv_slots, o_inv_name):
    # Update item amount chest (other inventory)
    other_inv_amount = max(min(from_slot[1] + to_slot[1], 64), 0)
    o_inv_slots[o_inv_slots.index(to_slot)] = (to_slot[0], other_inv_amount)
    # Update item amount agent inventory
    item_amount = (0, (from_slot[1] + to_slot[1]) - 64)[from_slot[1] + to_slot[1] > 64]
    item_slots[item_slots.index(from_slot)] = (from_slot[0], item_amount)

    return "combineInventoryItems " + o_inv_name + ":" + str(to_slot[0]) + " inventory:" + str(from_slot[0]), \
           item_slots, o_inv_slots


# Use Malmo's swap option if it's possible
def SwapSlotsWithAgent(indices_used, item_slots, o_inv_slots, o_inv_name, o_inv_size, from_slot):
    for x in range(o_inv_size):
        if x not in indices_used:
            indices_used.append(x)
            o_inv_slots.append((x, from_slot[1]))
            # It's swapped/zero, so not applicable anymore
            item_slots[next(item_slots.index(x) for x in item_slots if x[0] == from_slot[0])] = (from_slot[0], 0)
            return "swapInventoryItems inventory:" + str(from_slot[0]) + " " + o_inv_name + ":" + str(x), \
                   indices_used, item_slots, o_inv_slots
    return "", indices_used, item_slots, o_inv_slots
