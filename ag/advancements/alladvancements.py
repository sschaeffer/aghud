#!/usr/bin/env python3

from sys import path

path.append("/home/integ/Code/aghud")

from ag.common.aghudconstants import AGHUDConstants
from ag.common.aghudconfig import AGHUDConfig

import logging
import glob
import json
#Test Test

logger = logging.getLogger('alladvancements')

class Advancement():

    def __init__(self, filename):
        self._filename = filename
        self._parent = ""

    def read_advancement(self):
        advancement_file = open(self._filename,'r')
        advancement_info = json.load(advancement_file)
        advancement_file.close()

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
        print(self._parent +":\t\t\t"+self._filename)


class AllAdvancements():

    def __init__(self, aghudconfig):
        logger.debug(aghudconfig.worldname())
        files = glob.glob("/home/integ/Code/aghud/ag/advancements/vanilla_1.8.2/**/*.json", recursive=True)
        for file in files:
            advancement = Advancement(file)
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
