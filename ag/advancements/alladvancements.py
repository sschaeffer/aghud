#!/usr/bin/env python3

from sys import path

path.append("/home/integ/Code/aghud")

from ag.common.aghudconstants import AGHUDConstants
from ag.common.aghudconfig import AGHUDConfig

import logging
import glob

logger = logging.getLogger('alladvancements')

class AllAdvancements():

    def __init__(self, aghudconfig):
        logger.debug(aghudconfig.worldname())
        files = glob.glob("/home/integ/Code/aghud/ag/advancements/vanilla_1.8.2/**/*.json", recursive=True)
        print(files)

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
