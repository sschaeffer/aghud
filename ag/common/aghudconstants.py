
#!/usr/bin/python3

class AGHUDConstants():

    AUTO_DELAY_1MIN=1.0
    AUTO_DELAY_5MINS=300.0
    AUTO_DELAY_30MINS=1800.0
    AUTO_DELAY_1HR=3600.0

    SCHEDULER_DELAY=0.1
    LEVEL_FILE_UPDATE_LIMIT=AUTO_DELAY_5MINS+60.0
    AUTO_BACKUP_DEFAULT=True
    AUTO_BACKUP_DELAY_DEFAULT=AUTO_DELAY_5MINS*2
    AUTO_UPDATE_DEFAULT=True
    AUTO_UPDATE_DELAY_DEFAULT=AUTO_DELAY_1MIN

    MINIMUM_HEIGHT=20
    MINIMUM_WIDTH=40

    GAME_STARTING=0
    GAME_RUNNING=1
    GAME_RUNNING_NO_PLAYERS=2
    GAME_RUNNING_SINGLE_PLAYER=3
    GAME_PAUSED=4
    GAME_STOPPED=5
    GAME_RESET=6

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
    RAIN_NOSLEEP=23992       # 23992 No sleeping rainy days (19:59/9:33)
    DAY_FULLDAY=24000        # 24000 Full-day 

    COLOR_BCMENU_MENU=1
    COLOR_BCMENU_SELECTED_MENU=2
    COLOR_ADVANCEMENT_COMPLETE=3
    COLOR_STATUS_BAR=4
    COLOR_STATUS_BAR_GAME_TIME=5
    COLOR_STATUS_BAR_UNTIL_RAIN=6
    COLOR_STATUS_BAR_UNTIL_THUNDER=7

    COLOR_DAWN=101           # 1min 40secs
    COLOR_WORKDAY=102        # 5mins 50secs
    COLOR_HAPPYHOUR=103      # 2mins 30secs
    COLOR_TWILIGHT=104       # 27secs
    COLOR_SLEEP=105          # 21secs
    COLOR_MONSTERS=106       # 8mins 1secs
    COLOR_NO_MONSTERS=107    # 11 secs
    COLOR_NO_SLEEP=108       # 27secs



# ----
# UNIT TESTING ROUTINES - REMOVE BEFORE DEPLOYING RELEASE
# ----
def main():
    print()
    print("AGHUD Constants: Unit Testing")
    print(f"Minimum Height: {AGHUDConstants.MINIMUM_HEIGHT}")
    print(f"Minimum Width:  {AGHUDConstants.MINIMUM_WIDTH}")

if __name__ == "__main__":
    main()