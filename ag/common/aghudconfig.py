#!/usr/bin/python3
from sys import path
#path.append("/home/integ/Code/aghud")
path.append("C:/users/sscha/Code/aghud")

# Python wide imports
import os
import logging
from argparse import ArgumentParser
from pathlib import Path
from json import load, dump
import curses

# Package imports
from ag.common.aghudconstants import AGHUDConstants

class AGHUDConfig():

    __singleplayer = True
    __minecraftdir = ""
    __worldname = ""
    __servername = ""
    __advancementversion = "vanilla_1.8.2"
    __autobackup = AGHUDConstants.AUTO_BACKUP_DEFAULT
    __autobackupdelay = AGHUDConstants.AUTO_BACKUP_DELAY_DEFAULT
    __autoupdate = AGHUDConstants.AUTO_UPDATE_DEFAULT
    __autoupdatedelay = AGHUDConstants.AUTO_UPDATE_DELAY_DEFAULT


    def __init__(self, config_file, argv=None):

        config_data = None
        
        logging.debug(f"The config file is {config_file}")
        # Check the config file config.json
        if os.path.isfile(config_file) and os.access(config_file, os.R_OK):
            with open(config_file, "r") as jsonfile:
                config_data = load(jsonfile)
                jsonfile.close()

        if (config_data):
            if "singleplayer" in config_data: self.__singleplayer = config_data["singleplayer"]
            if "minecraftdir" in config_data: self.__minecraftdir = config_data["minecraftdir"]
            if "worldname" in config_data: self.__worldname = config_data["worldname"]
            if "servername" in config_data: self.__servername = config_data["servername"]
            if "advancementversion" in config_data: self.__advancementversion = config_data["advancementversion"]
            if "autobackup" in config_data: self.__autobackup = config_data["autobackup"]
            if "autobackupdelay" in config_data: self.__autobackupdelay = config_data["autobackupdelay"]
            if "autoupdate" in config_data: self.__autoupdate = config_data["autoupdate"]
            if "autoupdatedelay" in config_data: self.__autoupdatedelay = config_data["autoupdatedelay"]

        # Check the application arguments (they will override the config.json)
        parser = ArgumentParser(prog="aghud")
        parser.add_argument('--singleplayer', help="is this a single player world or server", action="store_true")
        parser.add_argument('--minecraftdir', help="minecraft server directory")
        parser.add_argument('--worldname', help="minecraft world name")
        parser.add_argument('--servername', help="minecraft server name")
        parser.add_argument('--advancementversion', help="minecraft advancement version")
        parser.add_argument('--autobackup', help="do you want to auto backup the world", action="store_true")
        parser.add_argument('--autobackupdelay', help="the amount of time between each auto backup")
        parser.add_argument('--noautoupdate', help="do you want to auto update aghud ", action="store_true")
        parser.add_argument('--autoupdatedelay', help="the amount of time between each auto update")
        args = parser.parse_args(argv)

        if(args.singleplayer):
            self.__singleplayer = True
            self.__minecraftdir = f"{Path.home()}/.minecraft"
        if(args.minecraftdir != None):
            self.__minecraftdir = args.minecraftdir
        if(args.worldname != None):
            self.__worldname = args.worldname
        if(args.servername != None):
            self.__servername = args.servername
        if(args.advancementversion != None):
            self.__advancementversion = args.advancementversion
        if(args.autobackup):
            self.__autobackup = True
        if(args.autobackupdelay):
            self.__autobackupdelay = args.autobackupdelay
        if(args.noautoupdate):
            self.__autoupdate = False
        if(args.autoupdatedelay):
            self.__autoupdatedelay = args.autoupdatedelay


    def write_aghud_config(self,config_file):

        if os.path.isfile(config_file) and not os.access(config_file, os.W_OK):
            print("config.json exists but can't be written to")
        else:
            with open(config_file,"w+") as jsonfile:
                output ={
                    "singleplayer": self.__singleplayer,
                    "minecraftdir": self.__minecraftdir,
                    "worldname": self.__worldname,
                    "servername": self.__servername,
                    "advancementversion": self.__advancementversion,
                    "autobackup": self.__autobackup,
                    "autobackupdelay": self.__autobackupdelay,
                    "autoupdate": self.__autoupdate,
                    "autoupdatedelay": self.__autoupdatedelay
                }
                dump(output,jsonfile,indent=4)
                jsonfile.close()

    def singleplayer(self):
        return self.__singleplayer

    def minecraftdir(self):
        return self.__minecraftdir

    def worldname(self):
        return self.__worldname

    def servername(self):
        return self.__servername

    def advancementversion(self):
        return self.__advancementversion

    def autobackup(self):
        return self.__autobackup

    def autobackupdelay(self):
        return self.__autobackupdelay

    def autoupdate(self):
        return self.__autoupdate

    def autoupdatedelay(self):
        return self.__autoupdatedelay

    def curses_setup(self, stdscr):

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.halfdelay(10)

        # Start colors in curses
        if curses.has_colors():
            curses.start_color()

            curses.init_pair(AGHUDConstants.COLOR_BCMENU_MENU, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(AGHUDConstants.COLOR_BCMENU_SELECTED_MENU, curses.COLOR_WHITE, curses.COLOR_BLACK)
            #if curses.can_change_color():
            if False:
                curses.init_pair(AGHUDConstants.COLOR_ADVANCEMENT_COMPLETE, 46, 0) #GREEN text and default bkgd
                curses.init_pair(AGHUDConstants.COLOR_STATUS_BAR, curses.COLOR_WHITE, 240) #BLACK text and GREY bkgd 
                curses.init_pair(AGHUDConstants.COLOR_STATUS_BAR_GAME_TIME, curses.COLOR_BLACK, 34) #BLACK text and BRIGHT GREEN bkgd 
                curses.init_pair(AGHUDConstants.COLOR_STATUS_BAR_UNTIL_RAIN, curses.COLOR_BLACK, 26) #BLACK text and  
                curses.init_pair(AGHUDConstants.COLOR_STATUS_BAR_UNTIL_THUNDER, curses.COLOR_CYAN, 237) #BLACK text and  

                curses.init_pair(AGHUDConstants.COLOR_DAWN, curses.COLOR_BLACK, 216)         # BLACK text and BRIGHT YELLOW bkgd (1min 40secs)
                curses.init_pair(AGHUDConstants.COLOR_WORKDAY, curses.COLOR_BLACK, 192)      # BLACK text and YELLOW bkgd (5mins 50secs)
                curses.init_pair(AGHUDConstants.COLOR_HAPPYHOUR, curses.COLOR_BLACK, 181)    # BLACK text and LIGHT BLUE/PURPLE bkgd (2mins 30secs)
                curses.init_pair(AGHUDConstants.COLOR_TWILIGHT, curses.COLOR_BLACK, 147)     # BLACK text and PURPLE bkgd (27secs)
                curses.init_pair(AGHUDConstants.COLOR_SLEEP, curses.COLOR_WHITE, 63)         # WHITE text and DARK BLUE PURPLE bkgd (21secs)
                curses.init_pair(AGHUDConstants.COLOR_MONSTERS, curses.COLOR_WHITE, 17)      # WHITE text and DARKEST BLUE/BLACK bkgd (8mins 1secs)
                curses.init_pair(AGHUDConstants.COLOR_NO_MONSTERS, curses.COLOR_WHITE, 20)   # WHITE text and LIGHT BLUE bkgd (11 secs)
                curses.init_pair(AGHUDConstants.COLOR_NO_SLEEP, curses.COLOR_WHITE, 96)      # WHITE text and PINK bkgd (27secs)
            else:
                curses.init_pair(AGHUDConstants.COLOR_ADVANCEMENT_COMPLETE, curses.COLOR_GREEN, 0) #GREEN text and default bkgd

    def check_minimum_size(self,stdscr:curses.window):
        (height,width) = stdscr.getmaxyx()
        if(height<AGHUDConstants.MINIMUM_HEIGHT or width<AGHUDConstants.MINIMUM_WIDTH):
            stdscr.clear()
            stdscr.addstr(int(height/2),int((width/2)-5),
                          f"Resize{AGHUDConstants.MINIMUM_HEIGHT}x{AGHUDConstants.MINIMUM_WIDTH}")
            stdscr.noutrefresh()
        return(height,width)




# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(aghudconfig):
    print()
    print("AGHUD Config:     Unit Testing")
    print(f"minecraftdir:       {aghudconfig.minecraftdir()}")
    print(f"worldname:          {aghudconfig.worldname()}")
    print(f"servername:         {aghudconfig.servername()}")
    print(f"singleplayer:       {aghudconfig.singleplayer()}")
    print(f"advancementversion: {aghudconfig.advancementversion()}")
    print(f"autobackup:         {aghudconfig.autobackup()}")
    print(f"autobackupdelay:    {aghudconfig.autobackupdelay()}")
    print(f"autoupdate:         {aghudconfig.autoupdate()}")
    print(f"autoupdatedelay:    {aghudconfig.autoupdatedelay()}")

    # Write config.json test
    print("Writing config.json")
    aghudconfig.write_aghud_config("/home/integ/Code/aghud/config.json")

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%I:%M:%S%p', level=logging.INFO)
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    main(aghudconfig)
