class InventoryItem:
    def __init__(self, name, subclass, tags):
        """
        Base class for all inventory items.
        :param name: Name of the item.
        :param subclass: Subclass or type of the item.
        :param tags: A list of tags that describe attributs of the item
        """
        self.name = name # name of the item
        self.subclass = subclass if subclass is not None else "none" # set default to ["none"] if no subclass is provided
        self.tags = tags if tags is not None else ["none"] # set default to ["none"] if no tags are provided

    def __repr__(self):
        return f"{self.subclass}: {self.name} (Tags: {', '.join(self.tags)})"
    
    def has_tag(self, tag):
        return tag in self.tags
    
    def matches_any_tags(self, tag_list):
        return any(tag in self.tags for tag in tag_list)
    

class Primary(InventoryItem):
    def __init__(self, name, subclass, onehand, tags):
        super().__init__(name, subclass, tags) # Inherit name, type and tags from Inventory Item
        self.onehand = onehand # Specific to Primary weapons, Can use the weapon one handed
    
    def __repr__(self):
        return f"{self.subclass}: {self.name}, (Tags: {', '.join(self.tags)}), One-Handed: {self.onehand}" # Override the default __repr__ from the base class.
    

class Secondary(InventoryItem):
    def __init__(self, name, subclass, tags):
        super().__init__(name, subclass, tags)


class Grenade(InventoryItem):
    def __init__(self, name, tags):
        super().__init__(name, "Grenade", tags)
    

class Armor(InventoryItem):
    def __init__(self, name, description, tags):
        super().__init__(name, "Armor", tags)
        self.description = description

    def __repr__(self):
        return f"{self.subclass}: {self.name}. {self.description}"
    
    
class Booster(InventoryItem):
    def __init__(self, name, description, tags):
        super().__init__(name, "Booster", tags)
        self.description = description

    def __repr__(self):
        return f"{self.subclass}: {self.name}. {self.description}"
    


class Stratagem(InventoryItem):
    def __init__(self, name, subclass, tags, image_name):
        super().__init__(name, subclass, tags)
        self.image_name = image_name # This will hold the iamge file path
    
    def assign_image(self, image_name):
        if image_name:
            return image_name
        else:
            if self.subclass == "Eagle":
                return "Libraries/Images/Blank/HD2-Blank-Eagle.png"
            elif self.subclass == "Sentry" or "Mines" or "Emplacement":
                return "Libraries/Images/Blank/HD2-Blank-Sentry.png"
            elif self.subclass == "Orbital":
                return "Libraries/Images/Blank/HD2-Blank-Orbital.png"
            elif self.subclass == "Support":
                if "support weapon" in self.tags:
                    return "Libraries/Images/Blank/HD2-Blank-Weapon.png"
                elif "backpack" in self.tags:
                    return "Libraries/Images/Blank/HD2-Blank-Packs.png"
            elif self.subclass == "Exosuit" or "Vehicle":
                return "Libraries/Images/Blank/HD2-Blank-Blue.png"
            else:
                return "Libraries/Images/Blank/HD2-Blank-Gold.png"
            
    def __repr__(self):
        return f"{self.subclass}: {self.name} (Tags: {', '.join(self.tags)}) {self.image_name}"

    
class Eagle(Stratagem):
    def __init__(self, name, tags, image_name):
        super().__init__(name, "Eagle", tags, image_name)

class Sentry(Stratagem):
    def __init__(self, name, subclass, tags, image_name):
        super().__init__(name, subclass, tags, image_name)

class Orbital(Stratagem):
    def __init__(self, name, tags, image_name):
        super().__init__(name, "Orbital", tags, image_name)


class Support(Stratagem):
    def __init__(self, name, tags, image_name):
        super().__init__(name, "Support", tags, image_name)

class Vehicle(Stratagem):
    def __init__(self, name, subclass, description, tags, image_name):
        super().__init__(name, subclass, tags, image_name)
        self.description = description