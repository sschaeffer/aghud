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

    def init_aghud(config_file, argv=None):

        minecraftdir = ""
        worldname = ""
        singleplayer = True
        autobackup = False
        autobackupdelay = 0.0

        config_data = None

        # Check the config file config.json
        if os.path.isfile(config_file) and os.access(config_file, os.R_OK):
            with open(config_file, "r") as jsonfile:
                config_data = load(jsonfile)
                jsonfile.close()

        if (config_data):
            if "minecraftdir" in config_data: minecraftdir = config_data["minecraftdir"]
            if "worldname" in config_data: worldname = config_data["worldname"]
            if "singleplayer" in config_data: singleplayer = config_data["singleplayer"]
            if "autobackup" in config_data: autobackup = config_data["autobackup"]
            if "autobackupdelay" in config_data: autobackupdelay = config_data["autobackupdelay"]

        # Check the application arguments (they will override the config.json)
        parser = ArgumentParser(prog="aghud")
        parser.add_argument('--minecraftdir', help="minecraft server directory")
        parser.add_argument('--worldname', help="minecraft world name")
        parser.add_argument('--singleplayer', help="is this a single player world or server", action="store_true")
        parser.add_argument('--autobackup', help="do you want to auto backup the world", action="store_true")
        parser.add_argument('--autobackupdelay', help="the amount of time between each auto backup")
        args = parser.parse_args(argv)

        if(args.singleplayer):
            singleplayer = True
            minecraftdir = f"{Path.home()}/.minecraft"
        if(args.minecraftdir != None):
            minecraftdir = args.minecraftdir
        if(args.worldname != None):
            worldname = args.worldname
        if(args.autobackup):
            autobackup = True
            autobackupdelay = AGHUDConstants.AUTO_BACKUP_DELAY_DEFAULT
        if(args.autobackupdelay):
            autobackupdelay = args.autobackupdelay
        return(minecraftdir, worldname, singleplayer, autobackup, autobackupdelay)


    def write_aghud_config(config_file, minecraftdir, worldname, singleplayer, autobackup, autobackupdelay):

        if os.path.isfile(config_file) and not os.access(config_file, os.W_OK):
            print("config.json exists but can't be written to")
        else:
            with open(config_file,"w+") as jsonfile:
                output ={
                    "minecraftdir": minecraftdir,
                    "worldname": worldname,
                    "singleplayer": singleplayer,
                    "autobackup": autobackup,
                    "autobackupdelay": autobackupdelay
                }
                dump(output,jsonfile,indent=4)
                jsonfile.close()



# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(minecraftdir, worldname, singleplayer, autobackup, autobackupdelay):
    print()
    print("AGHUD Config:    Unit Testing")
    print(f"minecraftdir:   {minecraftdir}")
    print(f"worldname:      {worldname}")
    print(f"singleplayer:   {singleplayer}")
    print(f"autobackup:       {autobackup}")
    print(f"autobackupdelay:  {autobackupdelay}")

    # Write config.json test
    print("\nWriting config.json")
    AGHUDConfig.write_aghud_config("/home/integ/Code/aghud/config.json", minecraftdir, worldname, singleplayer, autobackup, autobackupdelay)

if __name__ == "__main__":
    (minecraftdir, worldname, singleplayer, autobackup, autobackupdelay) = AGHUDConfig.init_aghud("/home/integ/Code/aghud/config.json")
    main(minecraftdir, worldname, singleplayer, autobackup, autobackupdelay)
