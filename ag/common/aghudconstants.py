
#!/usr/bin/python3

class AGHUDConstants():

    AUTO_BACKUP_5MINS=300.0
    AUTO_BACKUP_30MINS=1800.0
    AUTO_BACKUP_1HR=3600.0
    AUTO_BACKUP_DELAY_DEFAULT=AUTO_BACKUP_5MINS

    MINIMUM_HEIGHT=20
    MINIMUM_WIDTH=40

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