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

    def __init__(self, filename):
        self._filename = filename
        self._parent = ""
        self._title = ""
        self._name = ""
        self._section = ""
        self._isroot = False

    def parse_filename(self, filename):
        x = filename.split("/")[::-1]
        y = x.index('advancements')
        z = x[y-1::-1] 
        self._name = "/"
        self._name = self._name.join(z)
        self._section = x[y+1]

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

        print(self._section+": "+self._name)
        if self._parent == "":
            print(self._title+": "+self._filename)

class AllAdvancements():

    def __init__(self, aghudconfig):
        logger.debug(aghudconfig.worldname())

        # Check the advancement directory
        if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}").is_dir():
            if Path(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/datapacks").is_dir():
                datapacks = glob.glob(f"{aghudconfig.minecraftdir()}/saves/{aghudconfig.worldname()}/datapacks/*", recursive=True)
                for datapack in datapacks:
                    print(datapack)
            


        advancementdirs = glob.glob("./ag/advancements/bacap_1.13.4/**/advancements", recursive=True)
        for advancementdir in advancementdirs:
            jsonfiles = glob.glob(f"{advancementdir}/**/*.json", recursive=True)
            for jsonfile in jsonfiles:
                advancement = Advancement(jsonfile)
                advancement.read_advancement()

# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(aghudconfig):

    logging.getLogger("alladvancements").setLevel(logging.DEBUG)
 # ---   logging.getLogger("alladvancements").setLevel(logging.INFO)
    logger.debug("All Advancements:    Unit Testing")
    aa = AllAdvancements(aghudconfig)

if __name__ == "__main__":
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    main(aghudconfig)
