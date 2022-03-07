#!/usr/bin/python3
from sys import path
path.append("/home/integ/Code/aghud")

# Python wide imports
import os
import logging
from argparse import ArgumentParser
from pathlib import Path
from json import load, dump

# Package imports
from ag.common.aghudconstants import AGHUDConstants

class AGHUDConfig():

    __singleplayer = True
    __minecraftdir = ""
    __worldname = ""
    __servername = ""
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

    def autobackup(self):
        return self.__autobackup

    def autobackupdelay(self):
        return self.__autobackupdelay

    def autoupdate(self):
        return self.__autoupdate

    def autoupdatedelay(self):
        return self.__autoupdatedelay

# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(aghudconfig):
    print()
    print("AGHUD Config:     Unit Testing")
    print(f"minecraftdir:    {aghudconfig.minecraftdir()}")
    print(f"worldname:       {aghudconfig.worldname()}")
    print(f"servername:      {aghudconfig.servername()}")
    print(f"singleplayer:    {aghudconfig.singleplayer()}")
    print(f"autobackup:      {aghudconfig.autobackup()}")
    print(f"autobackupdelay: {aghudconfig.autobackupdelay()}")
    print(f"autoupdate:      {aghudconfig.autoupdate()}")
    print(f"autoupdatedelay: {aghudconfig.autoupdatedelay()}")

    # Write config.json test
    print("Writing config.json")
    aghudconfig.write_aghud_config("/home/integ/Code/aghud/config.json")

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%I:%M:%S%p', level=logging.INFO)
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    main(aghudconfig)
