#!/usr/bin/env python3

from operator import iadd
from reprlib import recursive_repr
from sys import path
from datetime import datetime

path.append("/home/integ/Code/aghud")
#path.append("C:/users/sscha/Code/aghud")

from ag.common.aghudconstants import AGHUDConstants
from ag.common.aghudconfig import AGHUDConfig

import logging
import glob
import json
from pathlib import Path


logger = logging.getLogger('alladvancements')

class Advancement():

    ADVANCEMENT_NOTCOMPLETED=0
    ADVANCEMENT_COMPLETED=1
    REQUIREMENT_ALL=0
    REQUIREMENT_ANY=1

    def __init__(self, filename):
        self._name = ""
        self._filename = filename
        self._title = ""
        self._parent = ""
        self._section = ""
        self._completed = self.ADVANCEMENT_NOTCOMPLETED
        self._criteria = []
        self._finished = []
        self._requirement = self.REQUIREMENT_ALL
        self._completed_datetime = "2010-01-01 00:00:00 +0900"
        self._printed = False
        self._has_trophy = False

    def parse_filename(self, filename):
        x = filename[:-5].rstrip().split("/")[::-1]
        y = x.index('advancements')
        z = x[y-1::-1] 
        self._name = "/"
        self._name = self._name.join(z)
        self._section = x[y+1]
        self._index = f"{self._section}:{self._name}"

    def read_advancement(self):
        advancement_file = open(self._filename,'r')
        advancement_info = json.load(advancement_file)
        advancement_file.close()

        self.parse_filename(self._filename)

        if 'display' not in advancement_info:
#            print ("No Display")
            pass
        elif 'title' not in advancement_info['display']:
#            print ("No Title")
            pass
        elif 'translate' not in advancement_info['display']['title']:
#            print ("No Translate")
            pass
        else:
            self._title = advancement_info['display']['title']['translate']
        if '.title' in self._title:
            newtitle = self._title.split('.')[-2]
            if newtitle == 'root':
                newtitle = self._title.split('.')[-3]
            self._title = newtitle

        if 'parent' not in advancement_info:
#            print ("No Parent")
            pass
        else:
            self._parent = advancement_info['parent']

        if 'criteria' not in advancement_info:
            print(f"No criteria for {self._name}")
            pass
        else:
            for criteria in advancement_info['criteria']:
                if criteria not in self._criteria:
                    self._criteria.append(criteria)

        if 'requirement' in advancement_info:
            self._requirement = self.REQUIREMENT_ANY

    def print_advancement(self):
        print(f"Advancement Name:      {self._name}")
        print(f"Advancement Filename:  {self._filename}")
        print(f"Advancement Title:     {self._title}")
        print(f"Advancement Parent:    {self._parent}")

        if(self._requirement==self.REQUIREMENT_ANY):
            print(f"Advancement Required:  ANY")
        else:
            print(f"Advancement Required:  ALL")

        print(f"Advancement Criteria:  ", end='')
        print(f"({len(self._criteria)}) ", end='')
        for criteria in self._criteria:
            print(f"{criteria} ", end='')
        print()

        print(f"Advancement Finished:  ", end='')
        print(f"({len(self._finished)}) ", end='')
        for criteria in self._finished:
            print(f"{criteria} ", end='')
        print()

        if(self._completed==self.ADVANCEMENT_COMPLETED):
            print(f"Advancement Completed: TRUE")
            print(f"Adveancement Completed Datatime: {self._completed_datetime}")
        else:
            print(f"Advancement Completed: FALSE")

    def index(self):
        return self._index

    def printed(self):
        return self._printed

    def set_printed(self,printed):
        self._printed = printed

    def has_trophy(self,trophy):
        self._has_trophy = trophy

    def print_for_spreadsheet(self):
        if(not self.printed()):
#            print(f"{self._completed} @@@ {self._title} @@@ {self._index} @@@ {self._completed_datetime[:-5]} @@@ {self._parent} @@@ {self._has_trophy}")
            if(self._completed and self._has_trophy):
                print(f"{self._completed} @@@ {self._title} @@@ {self._index} @@@ {self._completed_datetime[:-5]} @@@ {self._has_trophy}")
            self.set_printed(True)

class AllAdvancements():

    def __init__(self, aghudconfig):
        logger.debug(aghudconfig.worldname())

        self._advancements={}
        self._last_datetime = "2010-01-01 00:00:00 +0900"
        trophies={}

        # Check the advancement directory
        if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}").is_dir():
            if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/datapacks").is_dir():
                datapacks = glob.glob(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/datapacks/*", recursive=True)
        #        for datapack in datapacks:
        #            print(datapack)

        if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}").is_dir():
            if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/advancements").is_dir():
                self._useradvancementsdir = f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/advancements"

        if Path(f"./ag/advancements/{aghudconfig.advancementversion()}").is_dir():
            advancementdirs = glob.glob(f"./ag/advancements/{aghudconfig.advancementversion()}/**/advancements", recursive=True)

        if Path(f"./ag/advancements/{aghudconfig.advancementversion()}/data/bc_rewards/functions/trophy").is_dir():
            trophydirs = f"./ag/advancements/{aghudconfig.advancementversion()}/data/bc_rewards/functions/trophy"
            trophies = glob.glob(f"{trophydirs}/**/*.mcfunction")
#        print(len(trophies))

        for advancementdir in advancementdirs:
            jsonfiles = glob.glob(f"{advancementdir}/**/*.json", recursive=True)
            for jsonfile in jsonfiles:
                advancement = Advancement(jsonfile)
                advancement.read_advancement()
                for trophy in trophies:
                    if(advancement._name in trophy):
                        advancement.has_trophy(True)
                        break
                self._advancements[advancement.index()] = advancement
#        print(len(self._advancements))

    def update_advancements(self,user):
        filepath = Path(f"{self._useradvancementsdir}/{user}")
        if filepath.exists():
            advancementfh = filepath.open('r')
            useradvancements = json.load(advancementfh)
            advancementfh.close()

            for i in useradvancements:
                if not i.startswith("minecraft:recipes") and not i == "DataVersion":
                    if i in self._advancements:
                        if 'done' in useradvancements[i] and useradvancements[i]['done'] == True:
                            self._advancements[i]._completed = Advancement.ADVANCEMENT_COMPLETED
                        if 'criteria' in useradvancements[i]:
                            for criteria in useradvancements[i]['criteria']:
                                if criteria not in self._advancements[i]._finished:
                                    self._advancements[i]._finished.append(criteria)
                                    t1 = datetime.strptime(useradvancements[i]['criteria'][criteria],"%Y-%m-%d %H:%M:%S %z")
                                    t2 = datetime.strptime(self._advancements[i]._completed_datetime,"%Y-%m-%d %H:%M:%S %z")
                                    t3 = datetime.strptime(self._last_datetime,"%Y-%m-%d %H:%M:%S %z")
                                    if(t1>t2):
                                        self._advancements[i]._completed_datetime = useradvancements[i]['criteria'][criteria]
                                    if(t1>t3):
                                        self._last_datetime = useradvancements[i]['criteria'][criteria]

    def advancement_list(self, parent):
        returnlist=[]
        if parent == "":
            for i in self._advancements:
                if '/root' in i:
                    returnlist.append(i)
        else:
            for i in self._advancements:
                if self._advancements[i]._parent == parent:
                    if ':technical/' not in i:
                        returnlist.append(i)
                        returnlist.extend(self.advancement_list(i))
        return returnlist

    def advancement_title(self,advancement):
        return(self._advancements[advancement]._title)

    def advancement_complete(self,advancement):
        return(self._advancements[advancement]._completed)

    def print_advancements(self):
        for i in self._advancements:
            self._advancements[i].set_printed(False)
        self._advancements['blazeandcave:bacap/root'].print_for_spreadsheet()
        self._advancements['blazeandcave:bacap/getting_wood'].print_for_spreadsheet()
        self._advancements['minecraft:story/root'].print_for_spreadsheet()
        self._advancements['blazeandcave:bacap/time_to_mine'].print_for_spreadsheet()
        self._advancements['blazeandcave:bacap/time_to_strike'].print_for_spreadsheet()
        self._advancements['blazeandcave:bacap/time_to_chop'].print_for_spreadsheet()
        self._advancements['blazeandcave:bacap/time_to_dig'].print_for_spreadsheet()
        self._advancements['blazeandcave:bacap/time_to_farm'].print_for_spreadsheet()

        for i in self._advancements:
            if ':technical/' in i or '/obtain_netherite_hoe' in i:
                self._advancements[i].set_printed(True)

        print(f" @@@ @@@ Mining 109 @@@ @@@ ")
        self._advancements['blazeandcave:mining/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':mining/' in i or ':mining/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()
        self._advancements['minecraft:story/form_obsidian'].print_for_spreadsheet()
        self._advancements['minecraft:story/enter_the_nether'].print_for_spreadsheet()
        self._advancements['minecraft:story/iron_tools'].print_for_spreadsheet()
        self._advancements['minecraft:story/obtain_armor'].print_for_spreadsheet()
        self._advancements['minecraft:story/mine_diamond'].print_for_spreadsheet()
        self._advancements['minecraft:story/upgrade_tools'].print_for_spreadsheet()
        self._advancements['minecraft:story/enchant_item'].print_for_spreadsheet()
        self._advancements['minecraft:adventure/kill_mob_near_sculk_catalyst'].print_for_spreadsheet()
        self._advancements['minecraft:husbandry/wax_off'].print_for_spreadsheet()

        print(f" @@@ @@@ Building 107 @@@ @@@ ")
        self._advancements['blazeandcave:building/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':building/' in i or ':building/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()

        print(f" @@@ @@@ Farming 60 @@@ @@@ ")
        self._advancements['blazeandcave:farming/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':farming/' in i or ':farming/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()

        print(f" @@@ @@@ Animal 131 -133  @@@ @@@ ")
        self._advancements['minecraft:husbandry/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':animal/' in i or ':animal/' in self._advancements[i]._parent or \
                ':husbandry/' in i or ':husbandry/' in self._advancements[i]._parent:
                if '/truffle_worm' not in i and '/complete_catalogue' not in i and \
                    '/evelyn_evergreen' not in i and '/awards_ceremony' not in i and \
                    '/repair_wolf_armor' not in i and '/remove_wolf_armor' not in i and \
                    '/whole_pack' not in i and '/brush_armadillo' not in i and \
                    '/obtain_sniffer_egg' not in i and '/allay_deliver_item_to_player' not in i and \
                    '/allay_deliver_cake_to_note_block' not in i and '/plant_any_sniffer_seed' not in i and \
                    '/feed_snifflet' not in i:
                    if(not self._advancements[i].printed()):
                        self._advancements[i].print_for_spreadsheet()

        print(f" @@@ @@@ Monsters 78 -79 @@@ @@@ ")
        self._advancements['blazeandcave:monsters/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':monsters/' in i or ':monsters/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()

        print(f" @@@ @@@ Weaponry 49 @@@ @@@ ")
        self._advancements['blazeandcave:weaponry/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':weaponry/' in i or ':weaponry/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()
        self._advancements['minecraft:adventure/whos_the_pillager_now'].print_for_spreadsheet()

        print(f" @@@ @@@ Biomes 60 -61 @@@ @@@ ")
        self._advancements['blazeandcave:biomes/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':biomes/' in i or ':biomes/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()

        print(f" @@@ @@@ Adventure 116 -118  @@@ @@@ ")
        self._advancements['minecraft:adventure/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':adventure/' in i or ':adventure/' in self._advancements[i]._parent:
                if '/repair_wolf_armor' not in i and '/remove_wolf_armor' not in i and \
                    '/whole_pack' not in i and '/brush_armadillo' not in i and \
                    '/bullseye' not in i and '/read_power_of_chiseled_bookshelf' not in i and \
                    '/very_very_frightening' not in i and '/arbalistic'not in i and \
                    '/whos_the_pillager_now' not in i and '/spyglass_at_ghast' not in i and \
                    '/return_to_sender' not in i and \
                    '/spyglass_at_dragon' not in i:
                    if(not self._advancements[i].printed()):
                        self._advancements[i].print_for_spreadsheet()
        self._advancements['minecraft:husbandry/obtain_sniffer_egg'].print_for_spreadsheet()
        self._advancements['blazeandcave:adventure/truffle_worm'].print_for_spreadsheet()
        self._advancements['blazeandcave:adventure/evelyn_evergreen'].print_for_spreadsheet()
        self._advancements['blazeandcave:adventure/awards_ceremony'].print_for_spreadsheet()
        self._advancements['minecraft:husbandry/complete_catalogue'].print_for_spreadsheet()
        self._advancements['minecraft:husbandry/allay_deliver_item_to_player'].print_for_spreadsheet()
        self._advancements['minecraft:husbandry/allay_deliver_cake_to_note_block'].print_for_spreadsheet()
        self._advancements['minecraft:husbandry/plant_any_sniffer_seed'].print_for_spreadsheet()
        self._advancements['minecraft:husbandry/feed_snifflet'].print_for_spreadsheet()

        print(f" @@@ @@@ Redstone 47  @@@ @@@ ")
        self._advancements['blazeandcave:redstone/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':redstone/' in i or ':redstone/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()
        self._advancements['minecraft:adventure/bullseye'].print_for_spreadsheet()
        self._advancements['minecraft:adventure/read_power_of_chiseled_bookshelf'].print_for_spreadsheet()

        print(f" @@@ @@@ Enchanting 51 @@@ @@@ ")
        self._advancements['blazeandcave:enchanting/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':enchanting/' in i or ':enchanting/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()
        self._advancements['minecraft:adventure/very_very_frightening'].print_for_spreadsheet()
        self._advancements['minecraft:adventure/arbalistic'].print_for_spreadsheet()

        print(f" @@@ @@@ Statistics 58 -60 @@@ @@@ ")
        self._advancements['blazeandcave:statistics/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':statistics/' in i or ':statistics/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()

        print(f" @@@ @@@ Nether 106 -107 @@@ @@@ ")
        self._advancements['minecraft:nether/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':nether/' in i or ':nether/' in self._advancements[i]._parent:
                if '/a_much_more_doable_challenge' not in i and '/a_furious_test_subject' not in i and \
                    '/all_effects' not in i and '/all_potions' not in i:
                    self._advancements[i].print_for_spreadsheet()
        self._advancements['minecraft:adventure/spyglass_at_ghast'].print_for_spreadsheet()
        self._advancements['minecraft:nether/return_to_sender'].print_for_spreadsheet()
        self._advancements['minecraft:story/enter_the_end'].print_for_spreadsheet()

        print(f" @@@ @@@ Potion 27  @@@ @@@ ")
        self._advancements['blazeandcave:potion/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':potion/' in i or ':potion/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()
        self._advancements['minecraft:nether/all_potions'].print_for_spreadsheet()

        print(f" @@@ @@@ End 43 -44  @@@ @@@ ")
        self._advancements['minecraft:end/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':end/' in i or ':end/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()
        self._advancements['minecraft:adventure/spyglass_at_dragon'].print_for_spreadsheet()

        print(f" @@@ @@@ Challenges 38 -39  @@@ @@@ ")
        self._advancements['blazeandcave:challenges/root'].print_for_spreadsheet()
        for i in self._advancements:
            if ':challenges/' in i or ':challenges/' in self._advancements[i]._parent:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()

        print(f" @@@ @@@ Non-Characterized  @@@ @@@ ")

        for i in self._advancements:
            if ':technical/' not in i:
                if(not self._advancements[i].printed()):
                    self._advancements[i].print_for_spreadsheet()
#        self._advancements['minecraft:end/levitate'].print_advancement()

    def print_last_datetime(self):
        print(f"{self._last_datetime}")

    def print_number_of_completed(self):
        num_completed=0
        for i in self._advancements:
            if ':technical/' not in i and '/obtain_netherite_hoe' not in i:
                if self._advancements[i]._completed:
                    num_completed = num_completed+1
        print(f"{num_completed}")


# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(aghudconfig):

    logging.getLogger("alladvancements").setLevel(logging.DEBUG)
 # ---   logging.getLogger("alladvancements").setLevel(logging.INFO)
    logger.debug("All Advancements:    Unit Testing")
    aa = AllAdvancements(aghudconfig)
    aa.update_advancements(aghudconfig.uuidjson())

#    newlist=[]
#    newlist = aa.advancement_list('')
#    print(len(newlist))
#    for i in newlist:
#        print(f':{i}-{aa.advancement_title(i)}')
    aa.print_advancements()
    aa.print_last_datetime()
    aa.print_number_of_completed()

##    aa.show_root_categories()
##    aa.print_advancement_tree('blazeandcave:challenges/root')
##    aa._advancements['blazeandcave:challenges/i_am_loot'].print_advancement()

if __name__ == "__main__":
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    main(aghudconfig)
