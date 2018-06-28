from tools import inventory as inv

recipes = \
    {
        # Weapons
        "wooden_axe": [("planks", 3), ("stick", 2)],
        "wooden_pickaxe": [("planks", 3), ("stick", 2)],
        "stone_axe": [("cobblestone", 3), ("stick", 2)],
        "stone_pickaxe": [("cobblestone", 3), ("stick", 2)],

        # Raw materials
        "planks": [("log", 1)],
        "stick": [("planks", 1)]
    }


# Get the requested recipe if it exists
def GetRecipe(recipe_name):
    for key in recipes:
        if key == recipe_name:
            item = recipes.get(key)
            return item
    # print("There is no existing entry for item with name: " + str(recipe_name) + "!")
    return []


def IsRecipeInInventory(inventory, recipe_name):
    subcraft_items = []
    item = GetRecipe(recipe_name)

    for element in item:
        if inv.GetAmountOfType(inventory, element[0]) >= element[1]:
            continue
        elif inv.GetAmountOfType(inventory, element[0]) < element[1]:
            recipe = GetRecipe(element[0])
            if recipe is not None:
                for recipe_item in recipe:
                    if inv.GetAmountOfType(inventory, recipe_item[0]) >= recipe_item[1]:
                        subcraft_items.append(element[0])
                        continue
                    else:
                        # print("Complete sub-craft NOT possible!")
                        return False, []
    # print("Items are in inventory! Ready for crafting.")
    return True, subcraft_items


def GetMissingElements(inventory, recipe_name):
    missing_items = []
    item = GetRecipe(recipe_name)

    for element in item:
        amount = inv.GetAmountOfType(inventory, element[0])
        if amount < element[1]:
            missing_items.append((element[0], element[1]-amount))
            
    # print("The following items are missing: " + str(missing_items))
    return missing_items
