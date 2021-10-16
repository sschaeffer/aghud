
#!/usr/bin/python3

class AGHUDConstants():

    AUTO_DELAY_1MIN=1.0
    AUTO_DELAY_5MINS=300.0
    AUTO_DELAY_30MINS=1800.0
    AUTO_DELAY_1HR=3600.0

    AUTO_BACKUP_DEFAULT=True
    AUTO_BACKUP_DELAY_DEFAULT=AUTO_DELAY_5MINS
    AUTO_UPDATE_DEFAULT=True
    AUTO_UPDATE_DELAY_DEFAULT=AUTO_DELAY_1MIN

    MINIMUM_HEIGHT=20
    MINIMUM_WIDTH=40

    GAME_STARTING=0
    GAME_RUNNING=1
    GAME_RUNNING_NO_PLAYERS=2
    GAME_STOPPED=3
    GAME_RESET=4

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