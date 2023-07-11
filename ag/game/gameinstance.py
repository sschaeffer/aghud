#!/usr/bin/env python3
import subprocess
from sys import path

path.append("/home/integ/Code/aghud")

from ag.common.aghudconstants import AGHUDConstants
from ag.common.aghudconfig import AGHUDConfig
from ag.game.serverquery import ServerQuery
from ag.game.levelfile import LevelFile

#from ag.game.gamequery import GameQuery
#from bc.game.bclevelfile import BCLevelFile
#from bc.game.bcalladvancements import BCAllAdvancements
#from bc.game.bclogfiles import BCLogFiles
#from bc.game.bclog import BCLog

import logging
from time import sleep, time, ctime
from subprocess import call 
from pathlib import Path
from os import chdir, getcwd
from math import floor

logger = logging.getLogger('gameinstance')

class GameInstance():

    def __init__(self, aghudconfig):
        """
        Parameters
        ----------
        minecraftdir : str
            The path to the minecraft directory
        worldname : str
            The name of the current minecraft world
        ...
        """
        logger.debug("Creating game instance")
        self.set_singleplayer(aghudconfig.singleplayer())
        self.set_minecraftdir(aghudconfig.minecraftdir())
        self.set_worldname(aghudconfig.worldname())
        self.set_servername(aghudconfig.worldname())

        self.__server_query = ServerQuery()
        self.__level_file = LevelFile(aghudconfig)
        self.__game_status = AGHUDConstants.GAME_STARTING

        self.set_autobackup(aghudconfig.autobackup())
        self.set_autobackupdelay(aghudconfig.autobackupdelay())
        self.set_autoupdate(aghudconfig.autoupdate())
        self.set_autoupdatedelay(aghudconfig.autoupdatedelay())

        self.__last_update = 0.0
        self.__last_backup = time()


    def set_minecraftdir(self, minecraftdir):
        self.__minecraftdir = minecraftdir

    def set_worldname(self, worldname):
        self.__worldname = worldname

    def set_servername(self, servername):
        self.__servername = servername

    def set_singleplayer(self, singleplayer):
        self.__singleplayer = singleplayer

    def set_autoupdate(self, autoupdate):
        self.__autoupdate = autoupdate

    def set_autobackup(self, autobackup):
        self.__autobackup = autobackup

    def set_autoupdatedelay(self, autoupdatedelay):
        self.__autoupdatedelay = autoupdatedelay

    def set_autobackupdelay(self, autobackupdelay):
        self.__autobackupdelay = autobackupdelay


    def update_ready(self,current_time):
        if(self.__autoupdate):
            if current_time > self.__last_update + self.__autoupdatedelay:
               logger.debug(f"Update_ready: Current time {ctime(current_time)} > {ctime(self.__last_update + self.__autoupdatedelay)}")
               return True
        return False

    def backup_ready(self,current_time):
        if(self.__autobackup):
           if current_time > self.__last_backup + self.__autobackupdelay:
               return True
        return False

    def update(self,current_time):
        self.update_game_status(current_time)
        if self.__game_status == AGHUDConstants.GAME_RESET:
            logger.info("Game was reset, resetting level file")
            self.__level_file.reset()
            self.__game_status = AGHUDConstants.GAME_STARTING
        self.__level_file.update()
        self.__last_update = current_time

    def backup(self, current_time):
        self.update_game_status(current_time) 
        ## Make sure the game is still running
        ## If the game doesn't seem to be running skip the backup for now
        ##
        ## TODO Possibly changing this to elapsed time instead of skipping the backup
        ## Calculate how many actual minutes the game was running and backup based on that
        ##
        if self.__game_status == AGHUDConstants.GAME_RUNNING_SINGLE_PLAYER or self.__game_status == AGHUDConstants.GAME_RUNNING:
            self.backup_world()
            self.__last_backup = current_time
            logger.info( f"World Backup Completed")

 
    def update_game_status(self, current_time):
        '''
        Update Game function
        '''
        if self.__level_file.exists() and self.__level_file.region_directory_unchanged():
            if self.__singleplayer:
                if(current_time - self.__level_file.last_file_mod_time() < AGHUDConstants.LEVEL_FILE_UPDATE_LIMIT):
                    self.__game_status = AGHUDConstants.GAME_RUNNING_SINGLE_PLAYER
                else:
                    self.__game_status = AGHUDConstants.GAME_PAUSED
            else:
                #self.__server_query.test_connection(self.__minecraftdir, self.__servername)
                #if self.__server_query.is_connected():
                #    if self.__server_query.number_players() > 0:
                        self.__game_status = AGHUDConstants.GAME_RUNNING
                #    else:
                #        self.__game_status = AGHUDConstants.GAME_RUNNING_NO_PLAYERS
                #else:
                #    self.__game_status = AGHUDConstants.GAME_STOPPED
        else:
            if self.__game_status !=  AGHUDConstants.GAME_STARTING: self.__game_status = AGHUDConstants.GAME_RESET

    def game_status(self):
        if self.__game_status == AGHUDConstants.GAME_RUNNING:
            return("Game Running")
        elif self.__game_status == AGHUDConstants.GAME_RUNNING_NO_PLAYERS:
            return("Game Running (NP)")
        elif self.__game_status == AGHUDConstants.GAME_RUNNING_SINGLE_PLAYER:
            return("Game Running (S)")
        elif self.__game_status == AGHUDConstants.GAME_PAUSED:
            return("Game Paused")
        elif self.__game_status == AGHUDConstants.GAME_STOPPED:
            return("Game Stopped")
        elif self.__game_status == AGHUDConstants.GAME_RESET:
            return("Game Reset")
        else:
            return("Game Starting")

    def backup_world(self):

        if Path(f"{self.__minecraftdir}/saves").is_dir() and Path(f"{self.__minecraftdir}/backups").is_dir():
            currentdir = getcwd()
            expanded_minecraftdir=self.__minecraftdir.replace(' ','\ ')
            expanded_worldname=self.__worldname.replace(' ','\ ')
            command_line = ["bash",f"{currentdir}/ag/scripts/backup-world.bash",f"\"{expanded_minecraftdir}\"",f"\"{expanded_worldname}\""]

            chdir(f"{self.__minecraftdir}/saves")
            fstdout = open("/tmp/AGHUD-BACKUP-WORLD-SCRIPT","w+")

            call(command_line,stdout=fstdout,stderr=subprocess.DEVNULL)
            chdir(currentdir)

    def estimated_game_time(self,current_time=0):
        if current_time==0:
            current_time = time()
        result = self.__level_file.game_time()
        if self.__game_status == AGHUDConstants.GAME_RUNNING_SINGLE_PLAYER or self.__game_status == AGHUDConstants.GAME_RUNNING:
            if(result > 0):
                result = round(self.__level_file.game_time()+((current_time-self.__level_file.last_file_mod_time())*20))
        return(result)

    def estimated_day_time(self,current_time=0):
        if current_time==0:
            current_time = time()
        result = self.__level_file.day_time()
        if self.__game_status == AGHUDConstants.GAME_RUNNING_SINGLE_PLAYER or self.__game_status == AGHUDConstants.GAME_RUNNING:
            if(result > 0):
                result = round(self.__level_file.day_time()+((current_time-self.__level_file.last_file_mod_time())*20))
        return(result)

    def estimated_time_to_rain(self,current_time=0):
        if current_time==0:
            current_time = time()
        result = self.__level_file.rain_time()
        if self.__game_status == AGHUDConstants.GAME_RUNNING_SINGLE_PLAYER or self.__game_status == AGHUDConstants.GAME_RUNNING:
            result = round(self.__level_file.rain_time()-((current_time-self.__level_file.last_file_mod_time())*20))
        return(result)

    def estimated_is_raining_str(self,current_time=0):
        result=" "
        if self.__level_file.raining():
            if self.estimated_time_to_rain() >= 0:
                result="X"
        else:
            if self.estimated_time_to_rain() < 0:
                result="X"
        return(result)

    def estimated_time_to_rain_str(self):
        result = ""
        time_to_rain = round(self.estimated_time_to_rain()/20)
        result = f" {floor(time_to_rain/60):>2}:{floor(abs(time_to_rain)%60):02}"
        return result

    def estimated_time_to_thunder(self,current_time=0):
        if current_time==0:
            current_time = time()
        result = self.__level_file.thunder_time()
        if self.__game_status == AGHUDConstants.GAME_RUNNING_SINGLE_PLAYER or self.__game_status == AGHUDConstants.GAME_RUNNING:
            result = round(self.__level_file.thunder_time()-((current_time-self.__level_file.last_file_mod_time())*20))
        return(result)

    def estimated_is_thundering_str(self,current_time=0):
        result=" "
        if self.__level_file.thundering():
            if self.estimated_time_to_thunder() >= 0:
                result="X"
        else:
            if self.estimated_time_to_thunder() < 0:
                result="X"
        return(result)

    def estimated_time_to_thunder_str(self):
        result = ""
        time_to_thunder = round(self.estimated_time_to_thunder()/20)
        result = f"{floor(time_to_thunder/60):>2}:{floor(abs(time_to_thunder)%60):02}"
        return result

    def estimated_time_of_day(self):
        estdaytime = self.estimated_day_time()%AGHUDConstants.DAY_FULLDAY
        if estdaytime > AGHUDConstants.DAY_NOSLEEP:
            result = AGHUDConstants.NOSLEEP
        elif estdaytime > AGHUDConstants.DAY_NOMONSTERS:
            result = AGHUDConstants.NOMONSTERS     # duration 11 secs
        elif estdaytime > AGHUDConstants.DAY_MONSTERS:
            result = AGHUDConstants.MONSTERS       # duration 8mins 1secs
        elif estdaytime > AGHUDConstants.DAY_SLEEP:
            result = AGHUDConstants.SLEEP          # duration for 21secs
        elif estdaytime > AGHUDConstants.DAY_TWILIGHT:
            result = AGHUDConstants.TWILIGHT       # duration 27secs
        elif estdaytime > AGHUDConstants.DAY_HAPPYHOUR:
            result = AGHUDConstants.HAPPYHOUR      # duration 2mins 30secs
        elif estdaytime > AGHUDConstants.DAY_WORKDAY:
            result = AGHUDConstants.WORKDAY        # duration 5mins 50secs
        else:
            result = AGHUDConstants.DAWN           # duration 1min 40secs
        return(result)

    def estimated_time_of_day_str(self):
        result = "\u001b[38;5;216mDAWN\u001b[0m"
        estimated_time_of_day = self.estimated_time_of_day()
        if estimated_time_of_day == AGHUDConstants.WORKDAY:
            result = "\u001b[38;5;011mWORKDAY\u001b[0m"
        elif estimated_time_of_day == AGHUDConstants.HAPPYHOUR:
            result = "\u001b[38;5;181mHAPPYHOUR\u001b[0m"
        elif estimated_time_of_day == AGHUDConstants.TWILIGHT:
            result = "\u001b[38;5;147mTWILIGHT\u001b[0m"
        elif estimated_time_of_day == AGHUDConstants.SLEEP:
            result = "\u001b[38;5;063mSLEEP\u001b[0m"
        elif estimated_time_of_day == AGHUDConstants.MONSTERS:
            result = "\u001b[47m\u001b[38;5;017mMONSTERS\u001b[0m"
        elif estimated_time_of_day == AGHUDConstants.NOMONSTERS:
            result = "\u001b[47m\u001b[38;5;020mNO MONSTERS\u001b[0m"
        elif estimated_time_of_day == AGHUDConstants.NOSLEEP:
            result = "\u001b[38;5;096mNO SLEEP\u001b[0m"
#        result = "\u001b[38;5;216mDAWN\u001b[0m"+\
#            "\u001b[38;5;011mWORKDAY\u001b[0m"+\
#            "\u001b[38;5;181mHAPPYHOUR\u001b[0m"+\
#            "\u001b[38;5;147mTWILIGHT\u001b[0m"+\
#            "\u001b[38;5;063mSLEEP\u001b[0m"+\
#            "\u001b[47m\u001b[38;5;017mMONSTERS\u001b[0m"+\
#            "\u001b[47m\u001b[38;5;020mNO MONSTERS\u001b[0m"+\
#            "\u001b[38;5;096mNO SLEEP\u001b[0m"

        return result

    def estimated_time_before_transition(self):
        result = 0
        if self.estimated_time_of_day() >= AGHUDConstants.SLEEP:
            result = (AGHUDConstants.DAY_FULLDAY - (self.estimated_day_time()%AGHUDConstants.DAY_FULLDAY))/20
        else:
            result = (AGHUDConstants.DAY_SLEEP - (self.estimated_day_time()%AGHUDConstants.DAY_FULLDAY))/20
        return result

    def estimated_time_before_transition_str(self):
        result = ""
        time_before_transition = self.estimated_time_before_transition()
        time_before_transition = time_before_transition%AGHUDConstants.DAY_FULLDAY
        result = f"{floor(abs(time_before_transition)/60):>2}:{floor(abs(time_before_transition)%60):02}"
        return result

        



# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(aghudconfig):

    logging.getLogger("gameinstance").setLevel(logging.INFO)
    logging.getLogger("levelfile").setLevel(logging.INFO)

    logger.debug("Game Instance:    Unit Testing")

    game = GameInstance(aghudconfig)
    while(True):
        current_time = time()
        if game.update_ready(current_time):
            game.update(current_time)
            logger.info( f" {floor(game.estimated_day_time()/AGHUDConstants.DAY_FULLDAY)}.{game.estimated_day_time()%AGHUDConstants.DAY_FULLDAY} {game.estimated_time_before_transition_str()} {game.estimated_time_of_day_str()} {game.game_status()} {game.estimated_time_to_rain_str()}({game.estimated_is_raining_str()}) {game.estimated_time_to_thunder_str()}({game.estimated_is_thundering_str()})")
        if game.backup_ready(current_time):
            game.backup(current_time)
        sleep(AGHUDConstants.SCHEDULER_DELAY)

if __name__ == "__main__":
    aghudconfig = AGHUDConfig("/home/integ/Code/aghud/config.json")
    main(aghudconfig)
