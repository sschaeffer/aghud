#!/usr/bin/env python3
from sys import path
path.append("/home/integ/Code/aghud")

from ag.common.aghudconstants import AGHUDConstants
from ag.common.aghudconfig import AGHUDConfig
from ag.game.serverquery import ServerQuery

#from ag.game.gamequery import GameQuery
#from bc.game.bclevelfile import BCLevelFile
#from bc.game.bcalladvancements import BCAllAdvancements
#from bc.game.bclogfiles import BCLogFiles
#from bc.game.bclog import BCLog

from time import sleep, time
from subprocess import run 
from pathlib import Path

class GameInstance():

    def __init__(self, minecraftdir, worldname, singleplayer,
                 autobackup=AGHUDConstants.AUTO_BACKUP_DEFAULT,
                 autobackupdelay=AGHUDConstants.AUTO_BACKUP_DELAY_DEFAULT,
                 autoupdate=AGHUDConstants.AUTO_UPDATE_DEFAULT,
                 autoupdatedelay=AGHUDConstants.AUTO_UPDATE_DELAY_DEFAULT):
        """
        Parameters
        ----------
        minecraftdir : str
            The path to the minecraft directory
        worldname : str
            The name of the current minecraft world
        ...
        """
        self.set_minecraftdir(minecraftdir)
        self.set_worldname(worldname)
        self.set_servername(worldname)
        self.set_singleplayer(singleplayer)

        self._server_query = ServerQuery()
        self._game_port = 0
        self._game_status = AGHUDConstants.GAME_STARTING

        self.set_autobackup(autobackup)
        self.set_autobackupdelay(autobackupdelay)
        self.set_autoupdate(autoupdate)
        self.set_autoupdatedelay(autoupdatedelay)

        self._last_update = 0.0
        self._last_backup = 0.0

    def set_minecraftdir(self, minecraftdir):
        self._minecraftdir = minecraftdir

    def set_worldname(self, worldname):
        self._worldname = worldname

    def set_servername(self, servername):
        self._servername = servername

    def set_singleplayer(self, singleplayer):
        self._singleplayer = singleplayer

    def set_autoupdate(self, autoupdate):
        self._autoupdate = autoupdate

    def set_autobackup(self, autobackup):
        self._autobackup = autobackup

    def set_autoupdatedelay(self, autoupdatedelay):
        self._autoupdatedelay = autoupdatedelay

    def set_autobackupdelay(self, autobackupdelay):
        self._autobackupdelay = autobackupdelay


    def update_ready(self):
        if(self._autoupdate):
           if time() > self._last_update + self._autoupdatedelay:
               return True
        return False

    def backup_ready(self):
        if(self._autobackup):
           if time() > self._last_backup + self._autobackupdelay:
               return True
        return False

    def update(self):
        self.update_game_status()
        self._last_update = time()

    def backup(self):
        self._last_backup = time()

 
    def update_game_status(self):
        """
        if not singleplayer
            query status via network
        """
        if(Path(f"{self._minecraftdir}/saves/{self._worldname}").is_dir()):
            print(f"{self._minecraftdir}/saves/{self._worldname} is a directory")
            levelfile_path=Path(f"{self._minecraftdir}/saves/{self._worldname}/level.dat")
            if(levelfile_path.is_file()):
                print(f"{levelfile_path} is a file")
                if self._singleplayer:
                    self._game_status = AGHUDConstants.GAME_RUNNING
                else:
                    if not self._server_query.is_connected():
                        self._server_query.connect(self._minecraftdir, self._servername)

            else:
                if self._game_status !=  AGHUDConstants.GAME_STARTING: self._game_status = AGHUDConstants.GAME_RESET
        else:
            print(f"{self._minecraftdir}/saves/{self._worldname} is not a directory")
            if self._game_status !=  AGHUDConstants.GAME_STARTING: self._game_status = AGHUDConstants.GAME_RESET

# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main(minecraftdir, worldname, singleplayer, autobackup, autobackupdelay):

    print()
    print("Game Instance:    Unit Testing")

    game = GameInstance(minecraftdir,worldname,singleplayer,autobackup,autobackupdelay)
    game.set_autoupdate(True)
    game.set_autoupdatedelay(2.0)
    game.set_autobackup(True)
    game.set_autobackupdelay(5.0)

    while(True):
        print("loop")
        if game.update_ready():
            print("Update")
            game.update()
        if game.backup_ready():
            print("Backup")
            game.backup()
        sleep(.4)


if __name__ == "__main__":
    (minecraftdir, worldname, singleplayer, autobackup, autobackupdelay) = AGHUDConfig.init_aghud("/home/integ/Code/aghud/config.json")
    main(minecraftdir, worldname, singleplayer, autobackup, autobackupdelay)
