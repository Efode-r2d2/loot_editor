import xml.etree.ElementTree as ET
from model.item import Item


class XMLParser(object):
    def __init__(self, string_data):
        self.string_data = string_data
        self.xml = ET.fromstring(self.string_data)
        self.mod_prefixes = ["Mass", "GP_", "gp_", "FP4_"]
        self.not_gun_keywords = ["lrs", "ammo", "optic", "sawed", "suppressor", "goggles", "mag", "light", "rnd",
                                 "bayonet", "railatt", "compensator", "drum", "palm", "STANAG", "buttstock", "bttstck",
                                 "handguard", "hndgrd"]

    def get_items(self):
        items = list()
        for item_value in self.xml.iter('type'):
            item = Item()
            usages = list()
            tiers = list()
            item.name = item_value.attrib['name']
            for i in item_value:
                if i.tag == 'nominal':
                    item.nominal = i.text
                elif i.tag == 'restock':
                    item.restock = i.text
                elif i.tag == 'min':
                    item.min = i.text
                elif i.tag == 'category':
                    category = i.attrib['name']
                    if category != 'weapons':
                        item.item_type = category
                    else:
                        item.item_type = self.__get_type(name=item.name)
                elif i.tag == 'lifetime':
                    item.lifetime = i.text
                elif i.tag == 'usage':
                    usages.append(i.attrib['name'])
                elif i.tag == 'value':
                    tiers.append(i.attrib['name'])
                elif i.tag == 'flags':
                    item.dynamic_event = i.attrib['deloot']
                    item.count_in_hoarder = i.attrib['count_in_hoarder']
                    item.count_in_cargo = i.attrib['count_in_cargo']
                    item.count_in_player = i.attrib['count_in_player']
                    item.count_in_map = i.attrib['count_in_map']
            item.usage = ",".join(usages)
            item.tire = ",".join(tiers)
            items.append(item)
        return items

    def __get_type(self, name):
        if self.__is_gun(name=name):
            return "gun"
        if self.__is_ammo(name=name):
            return "ammo"
        if self.__is_mag(name=name):
            return "mag"
        if self.__is_optics(name=name):
            return "optic"
        return "attachment"

    def __is_gun(self, name):
        is_gun = True
        name = self.__remove_mod_prefix(name=name)
        for keyword in self.not_gun_keywords:
            if keyword in name.lower():
                is_gun = False
                break
        return is_gun

    def __is_mag(self, name):
        if "mag" in name.lower():
            return True
        else:
            return False

    def __is_ammo(self, name):
        if "ammo" in name.lower():
            return True
        else:
            return False

    def __is_optics(self, name):
        name = name.lower()
        if "optic" in name or "lrs" in name:
            return True
        else:
            return False

    def __remove_mod_prefix(self, name):
        for prefix in self.mod_prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
        return name
