#!/usr/bin/env python3

from reprlib import recursive_repr
from sys import path

path.append("/home/integ/Code/aghud")

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

    def __init__(self, filename):
        self._name = ""
        self._filename = filename
        self._title = ""
        self._parent = ""
        self._section = ""
        self._completed = self.ADVANCEMENT_NOTCOMPLETED

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
 
        if 'parent' not in advancement_info:
#            print ("No Parent")
            pass
        else:
            self._parent = advancement_info['parent']

    def index(self):
        return self._index

class AllAdvancements():

    def __init__(self, aghudconfig):
        logger.debug(aghudconfig.worldname())

        self._advancements={}

        # Check the advancement directory
        if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}").is_dir():
            if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/datapacks").is_dir():
                datapacks = glob.glob(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/datapacks/*", recursive=True)
                for datapack in datapacks:
                    print(datapack)

        if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}").is_dir():
            if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/advancements").is_dir():
                self._useradvancementsdir = f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/advancements"

        advancementdirs = glob.glob("./ag/advancements/bacap_1.13.4/**/advancements", recursive=True)
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

    def print_advancements(self):
        for i in self._advancements:
            print(f"{self._advancements[i]._completed} @@@ {self._advancements[i]._title} @@@ {i}")


# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(aghudconfig):

    logging.getLogger("alladvancements").setLevel(logging.DEBUG)
 # ---   logging.getLogger("alladvancements").setLevel(logging.INFO)
    logger.debug("All Advancements:    Unit Testing")
    aa = AllAdvancements(aghudconfig)
    aa.update_advancements('de3bf147-8c46-4698-81e1-ca2ef0a3e02d.json')
    aa.print_advancements()

if __name__ == "__main__":
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    main(aghudconfig)
