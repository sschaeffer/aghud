execute if score reward bac_settings matches 1 run give @s minecraft:crimson_fungus 8
execute if score reward bac_settings matches 1 run tellraw @s {"color":"green","text":" +8 Crimson Fungus"}
execute if score reward bac_settings matches 1 run give @s minecraft:warped_fungus 8
execute if score reward bac_settings matches 1 run tellraw @s {"color":"green","text":" +8 Warped Fungus"}
execute if score reward bac_settings matches 1 run tellraw @s {"color":"blue","text":" +50 Experience"}
scoreboard players add @s bac_advancements 1
