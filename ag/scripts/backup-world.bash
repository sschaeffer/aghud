#!/usr/bin/bash

minecraftdir=~/.minecraft
worldname='New\ World'

MINECRAFTDIR=${1:-$minecraftdir}
WORLDNAME=${2:-$worldname}

BACKUPDATE=`date +'%Y-%m-%d_%H-%M-%S'`

cd ${MINECRAFTDIR}/saves
pwd
eval /usr/bin/zip -r \"${MINECRAFTDIR}/backups/${WORLDNAME}_${BACKUPDATE}.zip\" \"${WORLDNAME}\"