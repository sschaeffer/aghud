#Prevents lag
gamerule doTileDrops false

#Destroys chunk
fill -848 64 95 -831 50 79 minecraft:air destroy
fill -848 50 95 -831 30 79 minecraft:air destroy
fill -848 30 95 -831 10 79 minecraft:air destroy
fill -848 10 95 -831 0 79 minecraft:air destroy

#Destroys trees
fill -841 62 99 -826 72 75 minecraft:air destroy

#Last bit of land
fill -845 65 84 -840 65 79 minecraft:air destroy
setblock -843 65 81 minecraft:oak_log

#Blocks will drop again
gamerule doTileDrops true