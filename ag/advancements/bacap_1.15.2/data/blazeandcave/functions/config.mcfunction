tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}
tellraw @s {"color":"gray","bold":"false","text":" ","extra":[{"color":"yellow","bold":"false","translate":"Blaze"},{"color":"gray","bold":"false","translate":"and"},{"color":"aqua","bold":"false","translate":"Cave"},{"color":"gray","bold":"false","translate":"'s Advancements Pack Config"}]}

tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}

# Welcome Message
execute if score intro_msg bac_settings matches 1 run tellraw @s ["",{"text":"[ ✔ ]","color":"green","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/intro_msg_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable","color":"gold"}]}}," ",{"translate":"Welcome Message currently enabled","hoverEvent":{"action":"show_text","contents":["",{"translate":"The Welcome Message appears when a player logs into the world for the first time. On servers that already have a custom welcome message, this should be turned off","color":"#D1FFFD"}]}}]
execute unless score intro_msg bac_settings matches 1 run tellraw @s ["",{"text":"[ ❌ ]","color":"red","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/intro_msg_on"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable","color":"gold"}]}}," ",{"translate":"Welcome Message currently disabled","hoverEvent":{"action":"show_text","contents":["",{"translate":"The Welcome Message appears when a player logs into the world for the first time. On servers that already have a custom welcome message, this should be turned off","color":"#D1FFFD"}]}}]
# Item Rewards
execute if score reward bac_settings matches 1 run tellraw @s ["",{"text":"[✔]","color":"green"}," ",{"text":"[/]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_first"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable only for the first player to get an advancement","color":"gold"}]}}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_first_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for the first player on each team","color":"gold"}]}}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable for all players","color":"gold"}]}}," ",{"translate":"Item Rewards:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Item Rewards are a small amount of bonus items awarded upon completing some advancements","color":"#D1FFFD"}]}}," ",{"translate":"All players"}]
execute if score reward bac_settings matches -1 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_on"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for all players","color":"gold"}]}}," ",{"text":"[/]","color":"yellow"}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_first_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for the first player on each team","color":"gold"}]}}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable for all players","color":"gold"}]}}," ",{"translate":"Item Rewards:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Item Rewards are a small amount of bonus items awarded upon completing some advancements","color":"#D1FFFD"}]}}," ",{"translate":"First player only"}]
execute if score reward bac_settings matches -2 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_on"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for all players","color":"gold"}]}}," ",{"text":"[/]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_first"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable only for the first player to get an advancement","color":"gold"}]}}," ",{"text":"[O]","color":"aqua"}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable for all players","color":"gold"}]}}," ",{"translate":"Item Rewards:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Item Rewards are a small amount of bonus items awarded upon completing some advancements","color":"#D1FFFD"}]}}," ",{"translate":"First player on each team"}]
execute unless score reward bac_settings matches 1 unless score reward bac_settings matches -2..-1 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_on"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for all players","color":"gold"}]}}," ",{"text":"[/]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_first"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable only for the first player to get an advancement","color":"gold"}]}}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/item_rewards_first_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for the first player on each team","color":"gold"}]}}," ",{"text":"[❌]","color":"red"}," ",{"translate":"Item Rewards:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Item Rewards are a small amount of bonus items awarded upon completing some advancements","color":"#D1FFFD"}]}}," ",{"translate":"Disabled"}]
# Experience Rewards
execute if score exp bac_settings matches 1 run tellraw @s ["",{"text":"[✔]","color":"green"}," ",{"text":"[/]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_first"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable only for the first player to get an advancement","color":"gold"}]}}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_first_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for the first player on each team","color":"gold"}]}}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable for all players","color":"gold"}]}}," ",{"translate":"Experience Rewards:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Experience Rewards are awarded upon completing some advancements, adding directly to a player's XP count","color":"#D1FFFD"}]}}," ",{"translate":"All players"}]
execute if score exp bac_settings matches -1 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_on"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for all players","color":"gold"}]}}," ",{"text":"[/]","color":"yellow"}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_first_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for the first player on each team","color":"gold"}]}}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable for all players","color":"gold"}]}}," ",{"translate":"Experience Rewards:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Experience Rewards are awarded upon completing some advancements, adding directly to a player's XP count","color":"#D1FFFD"}]}}," ",{"translate":"First player only"}]
execute if score exp bac_settings matches -2 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_on"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for all players","color":"gold"}]}}," ",{"text":"[/]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_first"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable only for the first player to get an advancement","color":"gold"}]}}," ",{"text":"[O]","color":"aqua"}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable for all players","color":"gold"}]}}," ",{"translate":"Experience Rewards:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Experience Rewards are awarded upon completing some advancements, adding directly to a player's XP count","color":"#D1FFFD"}]}}," ",{"translate":"First player on each team"}]
execute unless score exp bac_settings matches 1 unless score exp bac_settings matches -2..-1 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_on"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for all players","color":"gold"}]}}," ",{"text":"[/]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_first"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable only for the first player to get an advancement","color":"gold"}]}}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/exp_rewards_first_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for the first player on each team","color":"gold"}]}}," ",{"text":"[❌]","color":"red"}," ",{"translate":"Experience Rewards:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Experience Rewards are awarded upon completing some advancements, adding directly to a player's XP count","color":"#D1FFFD"}]}}," ",{"translate":"Disabled"}]
# Trophies
execute if score trophy bac_settings matches 1 run tellraw @s ["",{"text":"[✔]","color":"green"}," ",{"text":"[/]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_first"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable only for the first player to get an advancement","color":"gold"}]}}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_first_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for the first player on each team","color":"gold"}]}}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable for all players","color":"gold"}]}}," ",{"translate":"Trophies:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Trophies are decorative items awarded upon completing some advancements, in particular challenges, super challenges and milestones","color":"#D1FFFD"}]}}," ",{"translate":"All players"}]
execute if score trophy bac_settings matches -1 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_on"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for all players","color":"gold"}]}}," ",{"text":"[/]","color":"yellow"}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_first_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for the first player on each team","color":"gold"}]}}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable for all players","color":"gold"}]}}," ",{"translate":"Trophies:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Trophies are decorative items awarded upon completing some advancements, in particular challenges, super challenges and milestones","color":"#D1FFFD"}]}}," ",{"translate":"First player only"}]
execute if score trophy bac_settings matches -2 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_on"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for all players","color":"gold"}]}}," ",{"text":"[/]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_first"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable only for the first player to get an advancement","color":"gold"}]}}," ",{"text":"[O]","color":"aqua"}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable for all players","color":"gold"}]}}," ",{"translate":"Trophies:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Trophies are decorative items awarded upon completing some advancements, in particular challenges, super challenges and milestones","color":"#D1FFFD"}]}}," ",{"translate":"First player on each team"}]
execute unless score trophy bac_settings matches 1 unless score trophy bac_settings matches -2..-1 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_on"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for all players","color":"gold"}]}}," ",{"text":"[/]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_first"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable only for the first player to get an advancement","color":"gold"}]}}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/trophies_first_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable for the first player on each team","color":"gold"}]}}," ",{"text":"[❌]","color":"red"}," ",{"translate":"Trophies:","hoverEvent":{"action":"show_text","contents":["",{"translate":"Trophies are decorative items awarded upon completing some advancements, in particular challenges, super challenges and milestones","color":"#D1FFFD"}]}}," ",{"translate":"Disabled"}]
# Cooperative Mode
#execute if score coop bac_settings matches 1 run tellraw @s ["",{"text":"[ ✔ ]","color":"green","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/coop_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable","color":"gold"}]}}," ",{"translate":"Cooperative Mode currently enabled"}]
#execute if score coop bac_settings matches 2 run tellraw @s ["",{"text":"[ ✔ ]","color":"green","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/coop_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable","color":"gold"}]}}," ",{"translate":"Cooperative Mode currently enabled"}]
#execute unless score coop bac_settings matches 1..2 run tellraw @s ["",{"text":"[ ❌ ]","color":"red","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/coop_ru_sure"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable","color":"gold"}]}}," ",{"translate":"Cooperative Mode currently disabled"}]

execute if score coop bac_settings matches 1 run tellraw @s ["",{"text":"[✔]","color":"green"}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/coop_ru_sure_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable Team Cooperative Mode","color":"gold"}]}}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/coop_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable Cooperative Mode","color":"gold"}]}}," ",{"translate":"Cooperative Mode currently enabled","hoverEvent":{"action":"show_text","contents":["",{"translate":"Cooperative Mode shares every advancement gained among every player","color":"#D1FFFD"},"\n",{"translate":"Team Cooperative Mode works similarly, but only shares among players of the same team","color":"aqua"}]}}]
execute if score coop bac_settings matches 2 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/coop_ru_sure"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable Cooperative Mode","color":"gold"}]}}," ",{"text":"[O]","color":"aqua"}," ",{"text":"[❌]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/coop_off"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to disable Cooperative Mode","color":"gold"}]}}," ",{"translate":"Team Cooperative Mode currently enabled","hoverEvent":{"action":"show_text","contents":["",{"translate":"Cooperative Mode shares every advancement gained among every player","color":"#D1FFFD"},"\n",{"translate":"Team Cooperative Mode works similarly, but only shares among players of the same team","color":"aqua"}]}}]
execute unless score coop bac_settings matches 1..2 run tellraw @s ["",{"text":"[✔]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/coop_ru_sure"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable Cooperative Mode","color":"gold"}]}}," ",{"text":"[O]","color":"gray","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/coop_ru_sure_team"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Click to enable Team Cooperative Mode","color":"gold"}]}}," ",{"text":"[❌]","color":"red"}," ",{"translate":"Cooperative Mode currently disabled","hoverEvent":{"action":"show_text","contents":["",{"translate":"Cooperative Mode shares every advancement gained among every player","color":"#D1FFFD"},"\n",{"translate":"Team Cooperative Mode works similarly, but only shares among players of the same team","color":"aqua"}]}}]


tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}
# Links to Completion Message, Scoreboard Display and Technical settings
tellraw @s ["",{"text":"[ »» ]","color":"blue","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/msg_settings"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Settings for what messages that appear upon completing each tier of advancement should appear","color":"#D1FFFD"},"\n",{"translate":"Click to view","color":"gold"}]}}," ",{"translate":"Advancement Completion Message Settings"}]
#tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}
tellraw @s ["",{"text":"[ »» ]","color":"gold","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/scoreboard_settings"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Settings for what type of scoreboard to display and where","color":"#D1FFFD"},"\n",{"translate":"Click to view","color":"gold"}]}}," ",{"translate":"Advancement Scoreboard Display Settings"}]
#tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}
tellraw @s ["",{"text":"[ »» ]","color":"red","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/technical_settings"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Functions for updating, resetting and revoking advancements","color":"#D1FFFD"},"\n",{"translate":"Click to view","color":"gold"}]}}," ",{"translate":"Technical Settings"}]
tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}
tellraw @s ["",{"text":"[ ? ]","color":"dark_green","clickEvent":{"action":"run_command","value":"/function blazeandcave:config/help_menu"},"hoverEvent":{"action":"show_text","contents":["",{"translate":"Need help understanding how the datapack, this config menu, or anything else works?","color":"#D1FFFD"},"\n",{"translate":"Click to view","color":"gold"}]}}," ",{"translate":"Help"}]
tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}