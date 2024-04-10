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
        else:
            print(f"Advancement Completed: FALSE")

        print(f"{self._completed_datatime}")


    def index(self):
        return self._index

class AllAdvancements():

    def __init__(self, aghudconfig):
        logger.debug(aghudconfig.worldname())

        self._advancements={}
        self._last_datetime = "2010-01-01 00:00:00 +0900"

        # Check the advancement directory
        if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}").is_dir():
            if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/datapacks").is_dir():
                datapacks = glob.glob(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/datapacks/*", recursive=True)
        #        for datapack in datapacks:
        #            print(datapack)

        if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}").is_dir():
            if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/advancements").is_dir():
                self._useradvancementsdir = f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/advancements"

        if aghudconfig.advancementversion() == "skyblock_4.10":
            advancementdirs = glob.glob("./ag/advancements/skyblock_4.10/**/advancements", recursive=True)
        elif aghudconfig.advancementversion() == "bacap_1.13.7":
            advancementdirs = glob.glob("./ag/advancements/bacap_1.13.7/**/advancements", recursive=True)
        elif aghudconfig.advancementversion() == "bacap_1.15.2":
            advancementdirs = glob.glob("./ag/advancements/bacap_1.15.2/**/advancements", recursive=True)
        elif aghudconfig.advancementversion() == "bacap_1.16.1":
            advancementdirs = glob.glob("./ag/advancements/bacap_1.16.1/**/advancements", recursive=True)
        elif aghudconfig.advancementversion() == "bacap_1.16.3":
            advancementdirs = glob.glob("./ag/advancements/bacap_1.16.3/**/advancements", recursive=True)
        else:
            advancementdirs = glob.glob("./ag/advancements/vanilla_1.8.2/**/advancements", recursive=True)

        for advancementdir in advancementdirs:
            jsonfiles = glob.glob(f"{advancementdir}/**/*.json", recursive=True)
            for jsonfile in jsonfiles:
                advancement = Advancement(jsonfile)
                advancement.read_advancement()
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
            print(f"{self._advancements[i]._completed} @@@ {self._advancements[i]._title} @@@ {i} @@@ {self._advancements[i]._completed_datetime[:-5]}")
#        self._advancements['minecraft:end/levitate'].print_advancement()

    def print_last_datetime(self):
        print(f"{self._last_datetime}")

    def print_number_of_completed(self):
        num_completed=0
        for i in self._advancements:
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

    newlist=[]
    newlist = aa.advancement_list('')
    print(len(newlist))
    for i in newlist:
        print(f':{i}-{aa.advancement_title(i)}')
    aa.print_advancements()
    aa.print_last_datetime()
    aa.print_number_of_completed()

##    aa.show_root_categories()
##    aa.print_advancement_tree('blazeandcave:challenges/root')
##    aa._advancements['blazeandcave:challenges/i_am_loot'].print_advancement()

if __name__ == "__main__":
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    main(aghudconfig)
