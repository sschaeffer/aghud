#!/usr/bin/python3
from sys import path
path.append("/home/integ/Code/aghud")

# Python wide imports
import os
from argparse import ArgumentParser
from pathlib import Path
from json import load, dump

# Package imports
from ag.common.aghudconstants import AGHUDConstants

class AGHUDConfig():

    _singleplayer = True
    _minecraftdir = ""
    _worldname = ""
    _servername = ""
    _autobackup = AGHUDConstants.AUTO_BACKUP_DEFAULT
    _autobackupdelay = AGHUDConstants.AUTO_BACKUP_DELAY_DEFAULT
    _autoupdate = AGHUDConstants.AUTO_UPDATE_DEFAULT
    _autoupdatedelay = AGHUDConstants.AUTO_UPDATE_DELAY_DEFAULT


    def __init__(self, config_file, argv=None):

        config_data = None

        # Check the config file config.json
        if os.path.isfile(config_file) and os.access(config_file, os.R_OK):
            with open(config_file, "r") as jsonfile:
                config_data = load(jsonfile)
                jsonfile.close()

        if (config_data):
            if "singleplayer" in config_data: self._singleplayer = config_data["singleplayer"]
            if "minecraftdir" in config_data: self._minecraftdir = config_data["minecraftdir"]
            if "worldname" in config_data: self._worldname = config_data["worldname"]
            if "servername" in config_data: self._servername = config_data["servername"]
            if "autobackup" in config_data: self._autobackup = config_data["autobackup"]
            if "autobackupdelay" in config_data: self._autobackupdelay = config_data["autobackupdelay"]
            if "autoupdate" in config_data: self._autoupdate = config_data["autoupdate"]
            if "autoupdatedelay" in config_data: self._autoupdatepdelay = config_data["autoupdatedelay"]

        # Check the application arguments (they will override the config.json)
        parser = ArgumentParser(prog="aghud")
        parser.add_argument('--singleplayer', help="is this a single player world or server", action="store_true")
        parser.add_argument('--minecraftdir', help="minecraft server directory")
        parser.add_argument('--worldname', help="minecraft world name")
        parser.add_argument('--servername', help="minecraft server name")
        parser.add_argument('--autobackup', help="do you want to auto backup the world", action="store_true")
        parser.add_argument('--autobackupdelay', help="the amount of time between each auto backup")
        parser.add_argument('--noautoupdate', help="do you want to auto update aghud ", action="store_false")
        parser.add_argument('--autoupdatedelay', help="the amount of time between each auto update")
        args = parser.parse_args(argv)

        if(args.singleplayer):
            self._singleplayer = True
            self._minecraftdir = f"{Path.home()}/.minecraft"
        if(args.minecraftdir != None):
            self._minecraftdir = args.minecraftdir
        if(args.worldname != None):
            self._worldname = args.worldname
        if(args.servername != None):
            self._servername = args.servername
        if(args.autobackup):
            self._autobackup = True
        if(args.autobackupdelay):
            self._autobackupdelay = args.autobackupdelay
        if(args.noautoupdate):
            self._autoupdate = False
        if(args.autoupdatedelay):
            self._autoupdatedelay = args.autoupdatedelay


    def write_aghud_config(self,config_file):

        if os.path.isfile(config_file) and not os.access(config_file, os.W_OK):
            print("config.json exists but can't be written to")
        else:
            with open(config_file,"w+") as jsonfile:
                output ={
                    "singleplayer": self._singleplayer,
                    "minecraftdir": self._minecraftdir,
                    "worldname": self._worldname,
                    "servername": self._servername,
                    "autobackup": self._autobackup,
                    "autobackupdelay": self._autobackupdelay,
                    "autoupdate": self._autoupdate,
                    "autoupdatedelay": self._autoupdatedelay
                }
                dump(output,jsonfile,indent=4)
                jsonfile.close()



# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(aghudconfig):
    print()
    print("AGHUD Config:     Unit Testing")
    print(f"minecraftdir:    {aghudconfig.get_minecraftdir()}")
    print(f"worldname:       {aghudconfig.get_worldname()}")
    print(f"singleplayer:    {aghudconfig.get_servername()}")
    print(f"singleplayer:    {aghudconfig.get_singleplayer()}")
    print(f"autobackup:      {aghudconfig.get_autobackup}")
    print(f"autobackupdelay: {aghudconfig.get_autobackupdelay}")
    print(f"autoupdate:      {aghudconfig.get_autoupdate}")
    print(f"autoupdatedelay: {aghudconfig.get_autoupatedelay}")

    # Write config.json test
    print("\nWriting config.json")
    aghudconfig.write_aghud_config("/home/integ/Code/aghud/config.json")

if __name__ == "__main__":
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    main(aghudconfig)
