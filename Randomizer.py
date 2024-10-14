import random
from Libraries.Primaries import primaries
from Libraries.Secondaries import secondaries
from Libraries.Grenades import grenades
from Libraries.Armors import armors
from Libraries.Boosters import boosters
from Libraries.Stratagems.Eagles import eagles
from Libraries.Stratagems.Orbitals import orbitals
from Libraries.Stratagems.Sentries import sentries
from Libraries.Stratagems.Supports import supports
from Libraries.Stratagems.Vehicles import vehicles

def randomize_items(
        primary_var, secondary_var, grenade_var, armor_var, booster_var,
        stratagem_var, one_support_var, g_support_var, one_backpack_var, g_backpack_var, 
        g_sentry_var, g_tank_var, g_explosive_var, one_vehicle_var, g_vehicle_var,
        primary_filter_states, secondary_filter_states, grenade_filter_states, armor_filter_states,
        booster_filter_states, sentry_filter_states, vehicle_filter_states
        ):
    loadout = {}
    fulfilled_tags = []
    stratagem_choices = []
    selected_stratagems = set() # Set to prevent duplicates

    def filter_pool(item_pool, filter_states):
        filtered_items = []
        for item in item_pool:
            # Exclude the item if its name exists in filter_states and its value is True
            if item.name not in filter_states or not filter_states[item.name]:  # Adjusted to use item.name
                filtered_items.append(item)
        return filtered_items

    # Helper function to select an item from a pool based on tags
    def select_stratagem(pool, tag=None):
        if tag:
            choices = [item for item in pool if tag in item.tags and item not in selected_stratagems]
            if choices:
                item = random.choice(choices)
                selected_stratagems.add(item)
                fulfilled_tags.extend(item.tags)
                limit_support()
                limit_backpack()
                limit_vehicle()
                return item
        else:
            choices = [item for item in pool if item not in selected_stratagems]
            if choices:
                item = random.choice(choices)
                selected_stratagems.add(item)
                fulfilled_tags.extend(item.tags)
                limit_support()
                limit_backpack()
                limit_vehicle()
                return item
        return None

    # Limit checks for support weapon
    def limit_support():
        if one_support_var and 'support weapon' in fulfilled_tags:
            # Remove items with the 'support weapon' tag from future choices
            for pool in stratagems_pools.values():
                pool[:] = [item for item in pool if 'support weapon' not in item.tags or item in selected_stratagems]

    # Limit checks for backpack
    def limit_backpack():
        if one_backpack_var and 'backpack' in fulfilled_tags:
            # Remove items with the 'backpack' tag from future choices
            for pool in stratagems_pools.values():
                pool[:] = [item for item in pool if 'backpack' not in item.tags or item in selected_stratagems]

    # Limit checks for vehicle
    def limit_vehicle():
        if one_vehicle_var and any(item in stratagem_choices for item in vehicles):
            # Remove all items from the vehicles pool from future choices
            for pool in stratagems_pools.values():
                pool[:] = [item for item in pool if item not in vehicles]

    # Check each checkbox and randomize an item if the checkbox is active
    if primary_var:
        primary_pool = primaries[:]  # Make a copy of the original primaries
        if primary_filter_states:
            filtered_primaries = filter_pool(primary_pool, primary_filter_states)  # Filter based on popup selection
            if filtered_primaries:  # Ensure there are items left after filtering
                primary_choice = random.choice(filtered_primaries)  # Randomly select from filtered pool
                loadout['Primary Weapon'] = primary_choice
                fulfilled_tags.extend(primary_choice.tags)  # Track tags for later use
            else:
                # No items left after filtering
                print("No available primary weapons after filtering.")  # Debugging line
        else:
            # If no filters are selected, choose from the original pool
            primary_choice = random.choice(primary_pool)  # Randomly select from the unfiltered pool
            loadout['Primary Weapon'] = primary_choice
            fulfilled_tags.extend(primary_choice.tags)  # Track tags for later use

    if secondary_var:
        secondary_pool = secondaries [:]
        if secondary_filter_states:
            filtered_secondaries = filter_pool(secondary_pool, secondary_filter_states)
            if filtered_secondaries:
                secondary_choice = random.choice(filtered_secondaries)
                loadout['Secondary Weapon'] = secondary_choice
                fulfilled_tags.extend(secondary_choice.tags)
            else:
                print("No available secondary weapons after filtering.")  # Debugging line
        else:
            secondary_choice = random.choice(secondary_pool)
            loadout['Secondary Weapon'] = secondary_choice
            fulfilled_tags.extend(secondary_choice.tags)

    if grenade_var:
        grenade_pool = grenades [:]
        if grenade_filter_states:
            filtered_grenades = filter_pool(grenade_pool, grenade_filter_states)
            if filtered_grenades:
                grenade_choice = random.choice(filtered_grenades)
                loadout['Grenade'] = grenade_choice
                fulfilled_tags.extend(grenade_choice.tags)
            else:
                print("No available grenades after filtering.")  # Debugging line
        else:
            grenade_choice = random.choice(grenade_pool)
            loadout['Grenade'] = grenade_choice
            fulfilled_tags.extend(grenade_choice.tags)

    if armor_var:
        armor_pool = armors [:]
        if armor_filter_states:
            filtered_armors = filter_pool(armor_pool, armor_filter_states)
            if filtered_armors:
                armor_choice=random.choice(filtered_armors)
                loadout['Armor'] = armor_choice
                fulfilled_tags.extend(armor_choice.tags)
            else:
                print("No available armors after filtering.")  # Debugging line
        else:
            armor_choice = random.choice(armor_pool)
            loadout['Armor'] = armor_choice
            fulfilled_tags.extend(armor_choice.tags)

    if booster_var:
        booster_pool = boosters [:]
        if booster_filter_states:
            filtered_boosters = filter_pool(booster_pool, booster_filter_states)
            if filtered_boosters:
                booster_choice = random.choice(filtered_boosters)
                loadout['Booster'] = booster_choice
                fulfilled_tags.extend(booster_choice.tags)
            else:
                print("No available boosters after filtering.")  # Debugging line
        booster_choice = random.choice(booster_pool)
        loadout['Booster'] = booster_choice
        fulfilled_tags.extend(booster_choice.tags)

    # # Debug
    # print("Eagles:", eagles)
    # print("Orbitals:", orbitals)
    # print("Sentries:", sentries)
    # print("Supports:", supports)
    # print("Vehicles:", vehicles)

    # Stratagem logic: Select 4 stratagems
    if stratagem_var:
        # Make a fresh copy of the stratagem pools at the start of the function call
        stratagems_pools = {
            'eagles': eagles[:],  # Use slicing to copy the list
            'orbitals': orbitals[:],
            'sentries': sentries[:],
            'supports': supports[:],
            'vehicles': vehicles[:]
        }

        # Apply filters immediately to the pools
        if sentry_filter_states:
            stratagems_pools['sentries'] = filter_pool(stratagems_pools['sentries'], sentry_filter_states)
        print("Sentries:", stratagems_pools['sentries']) # Debug Message
        if vehicle_filter_states:
            stratagems_pools['vehicles'] = filter_pool(stratagems_pools['vehicles'], vehicle_filter_states)
        print("Vehicles:", stratagems_pools['vehicles']) # Debug Message

        # Fulfill guaranteed stratagems based on user input
        if g_support_var and 'support weapon' not in fulfilled_tags:
            support_choice = select_stratagem(stratagems_pools['supports'], tag='support weapon')
            if support_choice:
                stratagem_choices.append(support_choice)

        if g_backpack_var and 'backpack' not in fulfilled_tags:
            backpack_choice = select_stratagem(stratagems_pools['supports'], tag='backpack')
            if backpack_choice:
                stratagem_choices.append(backpack_choice)

        if g_explosive_var and 'explosive' not in fulfilled_tags:
            explosive_choice = select_stratagem(stratagems_pools['eagles'] + stratagems_pools['orbitals'] + stratagems_pools['supports'] + stratagems_pools['vehicles'], tag='explosive')
            if explosive_choice:
                stratagem_choices.append(explosive_choice)

        if g_tank_var and 'anti-tank' not in fulfilled_tags:
            tank_choice = select_stratagem(stratagems_pools['eagles'] + stratagems_pools['orbitals'] + stratagems_pools['supports'] + stratagems_pools['vehicles'], tag='anti-tank')
            if tank_choice:
                stratagem_choices.append(tank_choice)

        # For Sentries and Vehicles, select any item from their class
        if g_sentry_var:
            sentry_choice = select_stratagem(stratagems_pools['sentries'])
            if sentry_choice:
                stratagem_choices.append(sentry_choice)

        if g_vehicle_var:
            vehicle_choice = select_stratagem(stratagems_pools['vehicles'])
            if vehicle_choice:
                stratagem_choices.append(vehicle_choice)

        # Add remaining stratagems to fill the 4 slots, without exceeding 4 total
        while len(stratagem_choices) < 4:
            available_stratagems = [
                item for pool in stratagems_pools.values() 
                for item in pool if item not in selected_stratagems
            ]
            if available_stratagems:
                random_choice = random.choice(available_stratagems)
                stratagem_choices.append(random_choice)
                selected_stratagems.add(random_choice)
                fulfilled_tags.extend(random_choice.tags)
                limit_support()  # Check support limit as well
                limit_backpack()  # Check backpack limit as well
                limit_vehicle()  # Check vehicle limit as well

        # Add stratagems to loadout
        loadout['Stratagems'] = stratagem_choices[:4]  # Ensure exactly 4

    # Output or return the loadout
    print("Generated Loadout:")
    for category, items in loadout.items():
        print(f"{category}:")
        if isinstance(items, list):  # Check if the items are in a list
            for item in items:
                print(f"  - {item}")
        else:  # For categories with only one item
            print(f"  - {items}")
    print("==========")

    return loadout