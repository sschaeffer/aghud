#!/usr/bin/env python3
import subprocess
from sys import path
path.append("/home/integ/Code/aghud")

from ag.game.nbt import NBTFile
from ag.common.aghudconstants import AGHUDConstants
from ag.common.aghudconfig import AGHUDConfig

from time import time
from pathlib import Path
from datetime import datetime

class LevelFile(NBTFile):

    DAWN=1           # LIGHT ORANGE (1min 40secs)
    WORKDAY=2        # LIGHT YELLOW (5mins 50secs)
    HAPPYHOUR=3      # LIGHT MAROON (2mins 30secs)
    TWILIGHT=4       # LIGHT PURPLE (27secs)
    SLEEP=5          # DARK BLUE (21secs)
    MONSTERS=6       # DARKEST BLUE/BLACK (8mins 1secs)
    NOMONSTERS=7     # BLUE (11 secs)
    NOSLEEP=8        # MAUVE (27secs)

    DAY_DAWN=0               #     0 DAWN Wakeup and Wander (0:00)
    DAY_WORKDAY=2000         #  2000 WORKDAY (1:40)
    DAY_HAPPYHOUR=9000       #  9000 HAPPY-HOUR (7:30)
    DAY_TWILIGHT=12001       # 12000 TWILIGHT/villagers sleep (10:00)
    RAIN_SLEEP=12010         # 12012 SLEEP on rainy days (10:00)
    DAY_SLEEP=12542          # 12542 SLEEP on normal days/mobs don't burn (10:27.1/0)
    RAIN_MONSTERS=12969      # 12969 Rainy day monsters (10:48.45/21)
    DAY_MONSTERS=13188       # 13188 Monsters (10:59.4/32)
    DAY_NOMONSTERS=22812     # 22812 No more monsters (19:00.6/8:33)
    RAIN_NOMONSTERS=23031    # 23031 No more rainy day monsters(19:11.55/8:44)
    DAY_NOSLEEP=23460        # 23460 No sleeping on normal days (19:33/9:06)
    RAIN_NOSLEEP=23992        # 23992 No sleeping rainy days (19:59/9:33)
    DAY_FULLDAY=24000        # 24000 Full-day 

    def __init__(self, minecraftdir="/media/local/Minecraft/server", servername="fury", worldname="fury", serveractive=False, serverstarttime=0):

        self._minecraftdir=minecraftdir
        self._servername=servername
        self._worldname=worldname
        self._levelfilename="level.dat"

        self._serveractive=serveractive
        self._serverstarttime=serverstarttime

        self._lastupdatetime=0
        self._seed=None
        self._gametime=0
        self._daytime=0
        self._clearweathertime=0
        self._raining=False
        self._raintime=0
        self._thundering=False
        self._thundertime=0
        self._wanderingtraderid="<empty>"
        self._wanderingtraderspawnchance=0
        self._wanderingtraderspawndelay=0
        self._bclogfile = None

    def level_filename(self):
        return(self._minecraftdir+"/"+self._servername+"/"+self._worldname+"/"+self._levelfilename)

    def level_file_last_update(self):
        return(self._lastupdatetime)

    def seed(self):
        return(self._seed)

    def game_time(self):
        return(self._gametime)

    def day_time(self):
        return(self._daytime)

    def clear_weather_time(self):
        return(self._clearweathertime)

    def raining(self):
        return(self._raining)

    def rain_time(self):
        return(self._raintime)

    def thundering(self):
        return(self._thundering)

    def thunder_time(self):
        return(self._thundertime)

    def wandering_trader_spawn_delay(self):
        return(self._wanderingtraderspawndelay)

    def wandering_trader_spawn_chance(self):
        return(self._wanderingtraderspawnchance)

    def wandering_trader_id(self):
        return(self._wanderingtraderid)


    def read_level_file(self, levelfilepath):

        if self._lastupdatetime != levelfilepath.stat().st_mtime:
        # file has changed so lets save the previous results

            self._lastupdatetime = levelfilepath.stat().st_mtime
            super(BCLevelFile, self).__init__(levelfilepath)

            if "seed" in self["Data"]["WorldGenSettings"]:
                self._seed=str(self["Data"]["WorldGenSettings"]["seed"])

            if "Time" in self["Data"]:
                self._gametime=int(str(self["Data"]["Time"]))

            if "DayTime" in self["Data"]:
                self._daytime=int(str(self["Data"]["DayTime"]))

            if "ClearWeatherTime" in self["Data"]:
                self._clearweathertime=int(str(self["Data"]["ClearWeatherTime"]))

            if "rainTime" in self["Data"]:
                self._raintime=int(str(self["Data"]["rainTime"]))

            if "thunderTime" in self["Data"]:
                self._thundertime=int(str(self["Data"]["thunderTime"]))

            if "WanderingTraderSpawnDelay" in self["Data"]:
                self._wanderingtraderspawndelay=int(str(self["Data"]["WanderingTraderSpawnDelay"]))

            if "WanderingTraderSpawnChance" in self["Data"]:
                self._wanderingtraderspawnchance=int(str(self["Data"]["WanderingTraderSpawnChance"]))

            if "WanderingTraderId" in self["Data"]:
                self._wanderingtraderid=str(self["Data"]["WanderingTraderId"])
            else:
                self._wanderingtraderid="<empty>"

            if "raining" in self["Data"]:
                self._raining=bool(int(str(self["Data"]["raining"])))

            if "thundering" in self["Data"]:
                self._thundering=bool(int(str(self["Data"]["thundering"])))

 
    def update_level_info(self,serveractive,serverstarttime):
        levelfilepath = Path(self.level_filename())
        if not levelfilepath.exists():
            # game was reset or hasn't started yet. level_dat doesn't exist
            # also re-read the logs from scratch
            self.__init__(minecraftdir=self._minecraftdir,
                          servername=self._servername,
                          worldname=self._worldname,
                          serveractive=serveractive,
                          serverstarttime=serverstarttime)
        else:
            self._serveractive = serveractive
            self._serverstarttime = serverstarttime
            self.read_level_file(levelfilepath)

    def estimated_game_time(self):
        result = 0
        if not self._serveractive:
            result = self.game_time()
        elif self._gametime > 0:
            result = round(self._gametime+((time()-self._lastupdatetime)*20))
        elif self._serverstarttime > 0:
            result = round(time()-self._serverstarttime)*20
        return result


    def estimated_day_time(self):
        result = 0
        if not self._serveractive:
            result = self.day_time()
        elif self._daytime > 0:
            # if self.daytime is less than zero or zero it means the game is still starting
            result = round(self._daytime+((time()-self._lastupdatetime)*20))
        elif self._serverstarttime > 0:
            result = round(time()-self._serverstarttime)*20
        return result

    def estimated_clear_weather_time(self):
        result=0
        if not self._serveractive:
            result = self.clear_weather_time()
        elif self._clearweathertime > 0:
            result = round(self._clearweathertime-((time()-self._lastupdatetime)*20))
        return result

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

    def estimated_time_of_day(self):
        estdaytime = self.estimated_day_time()%self.DAY_FULLDAY
        if estdaytime > self.DAY_NOSLEEP:
            result = self.NOSLEEP
        elif estdaytime > self.DAY_NOMONSTERS:
            result = self.NOMONSTERS     # LIGHT BLUE (11 secs)
        elif estdaytime > self.DAY_MONSTERS:
            result = self.MONSTERS       # DARKEST BLUE/BLACK (8mins 1secs)
        elif estdaytime > self.DAY_SLEEP:
            result = self.SLEEP          # DARK BLUE PURPLE (21secs)
        elif estdaytime > self.DAY_TWILIGHT:
            result = self.TWILIGHT       # PURPLE (27secs)
        elif estdaytime > self.DAY_HAPPYHOUR:
            result = self.HAPPYHOUR      # LIGHT BLUE/PURPLE (2mins 30secs)
        elif estdaytime > self.DAY_WORKDAY:
            result = self.WORKDAY        # YELLOW (5mins 50secs)
        else:
            result = self.DAWN           # BRIGHT YELLOW (1min 40secs)
        return(result)

#        elif estdaytime > self.DAY_NORAINMONSTERS:
#            result = self.NORAINMONSTERS # LIGHTER BLUE/PINK (22secs)
#        elif estdaytime > self.DAY_RAINMONSTERS:
#            result = self.RAINMONSTERS   # DARK BLUE (11secs)


# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(minecraftdir, worldname, singleplayer, autobackup, autobackupdelay):

    print("LevelFile: Unit Testing")
    bclevelfile = LevelFile()

    bclevelfile.update_level_info(False,0)
    if bclevelfile.level_file_last_update() == 0:
        print("No level.dat file")
#        print(bclevelfile.pretty_tree())

    print(f"Level Filename:      {bclevelfile.level_filename()}")
    print(f"Last Update Time:    {datetime.fromtimestamp(bclevelfile.level_file_last_update())}")
    print(f"Seed:                {bclevelfile.seed()}")
    print(f"Game Time:           {bclevelfile.game_time()}")
    print(f"Estimated Game Time: {bclevelfile.estimated_game_time()}")
    print(f"Day Time:            {bclevelfile.day_time()}")
    print(f"Estimated Day Time:  {bclevelfile.estimated_day_time()}")
    print(f"Clear Weather Time:  {bclevelfile.clear_weather_time()}")
    print(f"Estimated Clear Wea: {bclevelfile.estimated_clear_weather_time()}")
    print(f"Raining:             {bclevelfile.raining()}")
    print(f"Rain Time:           {bclevelfile.rain_time()}")
    print(f"Estimated Rain Time: {bclevelfile.estimated_rain_time()}")
    print(f"Thundering:          {bclevelfile.thundering()}")
    print(f"Thunder Time:        {bclevelfile.thunder_time()}")
    print(f"Estimated Thunder T: {bclevelfile.estimated_thunder_time()}")
    print(f"Wandering Trader Sp: {bclevelfile.wandering_trader_spawn_delay()}")
    print(f"Estimated Wandering: {bclevelfile.estimated_wandering_trader_spawn_delay()}")
    print(f"Wandering Trader Sp: {bclevelfile.wandering_trader_spawn_chance()}")
    print(f"Wandering Trader Id: {bclevelfile.wandering_trader_id()}")
    print(f"Estimated Time of D: {bclevelfile.estimated_time_of_day()}")


if __name__ == "__main__":
    (minecraftdir, worldname, singleplayer, autobackup, autobackupdelay) = AGHUDConfig.init_aghud("/home/integ/Code/aghud/config.json")
    main(minecraftdir, worldname, singleplayer, autobackup, autobackupdelay)