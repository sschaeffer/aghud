#!/usr/bin/env python3
import subprocess
from sys import path
path.append("/home/integ/Code/aghud")

from ag.game.nbt import NBTFile
from ag.common.aghudconstants import AGHUDConstants
from ag.common.aghudconfig import AGHUDConfig

import logging
from time import time,ctime
from pathlib import Path
from datetime import datetime

logger = logging.getLogger('levelfile')


class LevelFile(NBTFile):

    def __init__(self, aghudconfig):

        logger.debug('Creating level file')
        self.__minecraftdir=aghudconfig.minecraftdir()
        self.__worldname=aghudconfig.worldname()
        self.__region_directory_inode=0
        self.reset()

    def reset(self):
        self.__last_file_read_time=0
        self.__seed=None
        self.__game_time=0
        self.__day_time=0
        self.__raining=False
        self.__rain_time=0
        self.__thundering=False
        self.__thunder_time=0
        self.__wandering_trader_spawn_delay=0
        self.__wandering_trader_spawn_chance=0
        self.__wandering_trader_id="<empty>"
        self.__clear_weather_time=0

    def last_file_read_time(self):
        if(self.__last_file_read_time == 0):
            return("Never")
        else:
            return(ctime(self.__last_file_read_time))

    def seed(self):
        return(self.__seed)

    def game_time(self):
        return(self.__game_time)

    def day_time(self):
        return(self.__day_time)

    def raining(self):
        return(self.__raining)

    def rain_time(self):
        return(self.__rain_time)

    def thundering(self):
        return(self.__thundering)

    def thunder_time(self):
        return(self.__thunder_time)

    def wandering_trader_spawn_delay(self):
        return(self.__wandering_trader_spawn_delay)

    def wandering_trader_spawn_chance(self):
        return(self.__wandering_trader_spawn_chance)

    def wandering_trader_id(self):
        return(self.__wandering_trader_id)

    def clear_weather_time(self):
        return(self.__clear_weather_time)

    def exists(self):
        result = False
        if Path(f"{self.__minecraftdir}/saves/{self.__worldname}").is_dir():
            if Path(f"{self.__minecraftdir}/saves/{self.__worldname}/level.dat").is_file():
                result = True
        return result

    def region_directory_unchanged(self):
        result = False
        region_directory_path=Path(f"{self.__minecraftdir}/saves/{self.__worldname}/region")
        if region_directory_path.is_dir():
            new_region_directory_inode = region_directory_path.stat().st_ino
            logger.debug(f"old inode: {self.__region_directory_inode} new inode: {new_region_directory_inode}")
            if self.__region_directory_inode == new_region_directory_inode:
                result = True
            elif self.__region_directory_inode == 0:
                self.__region_directory_inode = new_region_directory_inode
                result = True
            else:
                self.__region_directory_inode = new_region_directory_inode
        else:
            self.__region_directory_inode=0
        return result

    def last_file_mod_time(self):
        return Path(f"{self.__minecraftdir}/saves/{self.__worldname}/level.dat").stat().st_mtime

    def update(self):
        level_file_path = Path(f"{self.__minecraftdir}/saves/{self.__worldname}/level.dat")
        if level_file_path.is_file():
            ### Has the file been modified since it was last read
            if self.__last_file_read_time != level_file_path.stat().st_mtime:
                self.read_level_file(level_file_path)
                self.__last_file_read_time = level_file_path.stat().st_mtime

    def read_level_file(self, levelfilepath):

        super(LevelFile, self).__init__(levelfilepath)

        if "seed" in self["Data"]["WorldGenSettings"]:
            self.__seed=str(self["Data"]["WorldGenSettings"]["seed"])

        if "Time" in self["Data"]:
            self.__game_time=int(str(self["Data"]["Time"]))

        if "DayTime" in self["Data"]:
            self.__day_time=int(str(self["Data"]["DayTime"]))

        if "raining" in self["Data"]:
            self.__raining=bool(int(str(self["Data"]["raining"])))

        if "rainTime" in self["Data"]:
            self.__rain_time=int(str(self["Data"]["rainTime"]))

        if "thundering" in self["Data"]:
            self.__thundering=bool(int(str(self["Data"]["thundering"])))

        if "thunderTime" in self["Data"]:
            self.__thunder_time=int(str(self["Data"]["thunderTime"]))

        if "WanderingTraderSpawnDelay" in self["Data"]:
            self.__wandering_trader_spawn_delay=int(str(self["Data"]["WanderingTraderSpawnDelay"]))

        if "WanderingTraderSpawnChance" in self["Data"]:
            self.__wandering_trader_spawn_chance=int(str(self["Data"]["WanderingTraderSpawnChance"]))

        if "WanderingTraderId" in self["Data"]:
            self.__wandering_trader_id=str(self["Data"]["WanderingTraderId"])
        else:
            self.__wandering_trader_id="<empty>"

        if "clearWeatherTime" in self["Data"]:
            self.__clear_weather_time=int(str(self["Data"]["clearWeatherTime"]))


 






    def estimated_rain_time(self):
        result = 0
        if not self._serveractive:
            result = self.rain_time()
        elif self._raintime != 0:
            result = round(self._raintime-((time()-self._lastupdatetime)*20))
        return result

    def estimated_thunder_time(self):
        result = 0
        if not self._serveractive:
            result = self.thunder_time()
        elif self._thundertime != 0:
            result = round(self._thundertime-((time()-self._lastupdatetime)*20))
        return result

    def estimated_wandering_trader_spawn_delay(self):
        result = 0
        if not self._serveractive:
            result = self.wandering_trader_spawn_delay()
        elif self._wanderingtraderspawndelay != 0:
            result = round(self._wanderingtraderspawndelay-((time()-self._lastupdatetime)*20))
        return result

    def estimated_is_raining(self):
        result = False 
        if self.raining and self.estimated_rain_time() > 0:
            result = True
        elif not self.raining and self.estimated_rain_time() < 0:
            result = True
        return(result)

    def estimated_is_thundering(self):
        result = False 
        if self.estimated_is_raining() and self.thundering and self.estimated_thunder_time() > 0:
            result = True
        elif self.estimated_is_raining() and not self.thundering and self.estimated_thunder_time() < 0:
            result = True
        return(result)

    def estimated_is_monsters(self):
        estdaytime = self.estimated_day_time()%self.DAY_FULLDAY
        result = False
        if estdaytime >= self.DAY_MONSTERS and estdaytime <= self.DAY_NOMONSTERS:
            result = True 
        return result 

    def estimated_is_bed_usable(self):
        estdaytime = self.estimated_day_time()%self.DAY_FULLDAY
        result = False
        if estdaytime >= self.DAY_SLEEP and estdaytime <= self.DAY_NOSLEEP:
            result = True 
        return result


# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(aghudconfig):

    logger.setLevel(logging.DEBUG)
    logger.debug("LevelFile: Unit Testing")
    levelfile = LevelFile(aghudconfig)

###    bclevelfile.update_level_info(False,0)
###    if bclevelfile.level_file_last_update() == 0:
###        print("No level.dat file")
###        print(bclevelfile.pretty_tree())

    logger.debug(f"Last read time:      {levelfile.last_file_read_time()}")
    logger.debug(f"Seed:                {levelfile.seed()}")
    logger.debug(f"Game Time:           {levelfile.game_time()}")
    logger.debug(f"Day Time:            {levelfile.day_time()}")
    logger.debug(f"Raining:             {levelfile.raining()}")
    logger.debug(f"Rain Time:           {levelfile.rain_time()}")
    logger.debug(f"Thundering:          {levelfile.thundering()}")
    logger.debug(f"Thunder Time:        {levelfile.thunder_time()}")
    logger.debug(f"Wandering Trader Sp: {levelfile.wandering_trader_spawn_delay()}")
    logger.debug(f"Wandering Trader Sp: {levelfile.wandering_trader_spawn_chance()}")
    logger.debug(f"Wandering Trader Id: {levelfile.wandering_trader_id()}")
    logger.debug(f"Clear Weather Time:  {levelfile.clear_weather_time()}")

    levelfile.update()

    logger.debug(f"Last read time:      {levelfile.last_file_read_time()}")
    logger.debug(f"Seed:                {levelfile.seed()}")
    logger.debug(f"Game Time:           {levelfile.game_time()}")
    logger.debug(f"Day Time:            {levelfile.day_time()}")
    logger.debug(f"Raining:             {levelfile.raining()}")
    logger.debug(f"Rain Time:           {levelfile.rain_time()}")
    logger.debug(f"Thundering:          {levelfile.thundering()}")
    logger.debug(f"Thunder Time:        {levelfile.thunder_time()}")
    logger.debug(f"Wandering Trader Sp: {levelfile.wandering_trader_spawn_delay()}")
    logger.debug(f"Wandering Trader Sp: {levelfile.wandering_trader_spawn_chance()}")
    logger.debug(f"Wandering Trader Id: {levelfile.wandering_trader_id()}")
    logger.debug(f"Clear Weather Time:  {levelfile.clear_weather_time()}")


###    if levelfile.exists():
###        print(f"Level file:          {levelfile.last_update()}")
###    else:
###        print(f"Level file does not exist")


###    print(f"Estimated Game Time: {bclevelfile.estimated_game_time()}")
###    print(f"Estimated Day Time:  {bclevelfile.estimated_day_time()}")
###    print(f"Estimated Clear Wea: {bclevelfile.estimated_clear_weather_time()}")
###    print(f"Estimated Rain Time: {bclevelfile.estimated_rain_time()}")
###    print(f"Estimated Thunder T: {bclevelfile.estimated_thunder_time()}")
###    print(f"Estimated Wandering: {bclevelfile.estimated_wandering_trader_spawn_delay()}")
###    print(f"Estimated Time of D: {bclevelfile.estimated_time_of_day()}")


if __name__ == "__main__":
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    main(aghudconfig)