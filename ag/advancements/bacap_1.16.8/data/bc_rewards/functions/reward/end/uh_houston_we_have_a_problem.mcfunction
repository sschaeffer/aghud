give @s minecraft:firework_rocket[minecraft:fireworks={flight_duration:1}] 32
tellraw @s {"color":"green","text":" +32 ","extra":[{"translate":"item.minecraft.firework_rocket"}]}
give @s minecraft:enchanted_book[minecraft:stored_enchantments={"minecraft:feather_falling":4}] 1
tellraw @s {"color":"green","text":" +1 ","extra":[{"translate":"enchantment.minecraft.feather_falling"},{"text":" "},{"translate":"enchantment.level.4"},{"text":" "},{"translate":"item.minecraft.enchanted_book"}]}
