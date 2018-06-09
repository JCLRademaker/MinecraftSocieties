from collections import namedtuple


# Put the items from the super-inventory in an InventoryObject and
# return the contents of the wanted inventory
def GetInventory(super_inventory, inventory_name, inventory_object):
    inventory = [inventory_object(**k) for k in super_inventory]
    sub_inventory = [x for x in inventory if x.inventory == inventory_name]
    return sub_inventory


def IsInventoryFull(inventory):
    if len(inventory) == 0:
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


# Retrieve item from inventory with item type if possible
def GetItemsFromInventory(inventory, item_type):
    item_slots = [(x.index, x.quantity) for x in inventory if x.type == item_type]
    return item_slots


def FindSlotsInUse(inventory, inventory_name):
    slots_in_use = [x.index for x in inventory if x.inventory == inventory_name]
    if type(slots_in_use) is not list:
        slots_in_use = [slots_in_use]
    return slots_in_use


# Combine slots if there are slots to combine
def CombineSlotsWithAgent(from_slot, other_inv_name, other_inv_item, item_amount):
    # Keep combining until you can no longer combine
    if item_amount > 0 and other_inv_item.quantity < 64:
        item_amount = (0, 64 - other_inv_item.quantity)[item_amount + other_inv_item.quantity > 64]
        return "combineInventoryItems " + other_inv_name + ":" + str(other_inv_item.index) + " inventory:" + str(
                from_slot), (from_slot, item_amount)
    return "", (-1, -1)


def CombineSlotWithAgent(from_slot, to_slot, other_inv_name):
    return "combineInventoryItems " + other_inv_name + ":" + str(to_slot) + " inventory:" + str(from_slot)


# Swap slots if slots cannot be combined
def SwapSlotsWithAgent(from_slot, other_inv_name, other_inv_size, indices_used):
    for x in range(0, other_inv_size):
        if x not in indices_used:
            indices_used.append(x)
            return "swapInventoryItems inventory:" + str(from_slot) + " " + other_inv_name + ":" + str(x), indices_used
    return "", other_inv_size
