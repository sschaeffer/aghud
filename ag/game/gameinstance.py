#!/usr/bin/env python3
from sys import path
path.append("/home/integ/Code/aghud")

from ag.common.aghudconstants import AGHUDConstants
import subprocess

#from ag.game.gamequery import GameQuery
#from bc.game.bclevelfile import BCLevelFile
#from bc.game.bcalladvancements import BCAllAdvancements
#from bc.game.bclogfiles import BCLogFiles
#from bc.game.bclog import BCLog

from time import sleep, time
from subprocess import run 

class GameInstance():

    def __init__(self, minecraftdir, worldname, singleplayer,
                 autobackup=AGHUDConstants.AUTO_BACKUP_DEFAULT,
                 autobackupdelay=AGHUDConstants.AUTO_BACKUP_DELAY_DEFAULT,
                 autoupdate=True, autoupdatedelay=1.0):
        """
        Parameters
        ----------
        minecraftdir : str
            The path to the minecraft directory
        worldname : str
            The name of the current minecraft world
        ...
        """
        self._minecraftdir=minecraftdir
        self._worldname=worldname
        self._singleplayer=singleplayer
        self._autobackup=autobackup
        self._autobackupdelay=autobackupdelay
        self._autoupdate=autoupdate
        self._autoupdatedelay=autoupdatedelay


