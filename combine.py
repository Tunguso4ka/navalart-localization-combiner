#!/bin/python3
from os     import system
from csv    import reader, writer

#loading pathes from config
file = open('config')
lines = file.readlines()
GameLocDir = lines[0].strip()
YourLocDir = lines[1].strip()
file.close()
print("Config loaded.")

#dictionary files
GameLoc     = {} #combined official game localization
YourLoc     = {} #your localization 
NewLoc      = {} #combined official and yours localization

#function that returns .csv localisation file as a dictionary
def ReturnLocList(path, doformat=False):
    with open(path) as file:
        rfile = reader(file)
        LocList = {}
        for i in rfile:
            if doformat: LocList[i[0]].strip() = i[2].strip()
            else: LocList[i[0]] = i[1]
        return LocList

#combining official game locals into one
#aircraftweapons.csv, parts.csv, mission.csv, tips.csv, tutorials.csv, aircraftweaponsDes.csv, descriptions.csv, languages.csv
GameLoc |= ReturnLocList(GameLocDir+"languages.csv", True)
GameLoc |= ReturnLocList(GameLocDir+"tips.csv", True)
GameLoc |= ReturnLocList(GameLocDir+"tutorials.csv", True)
GameLoc |= ReturnLocList(GameLocDir+"parts.csv", True)
GameLoc |= ReturnLocList(GameLocDir+"descriptions.csv", True)
GameLoc |= ReturnLocList(GameLocDir+"aircraftweapons.csv", True)
GameLoc |= ReturnLocList(GameLocDir+"aircraftweaponsDes.csv", True)
print(f"Loaded {len(GameLoc)} game localization lines.")

#getting your local
YourLoc |= ReturnLocList(YourLocDir+"languages.csv")
print(f"Loaded {len(YourLoc)} your localization lines.")

#combining both locals
NewLoc = GameLoc | YourLoc
print(f"Combined into {len(NewLoc)} new localization lines.")

#safety feature (WOW!)
res = input("Proceed? y/N - ")
if res not in "yY": exit()

#moving old local file and creating a new one from combined localization
system(f"mv {YourLocDir}languages.csv {OldLocDir}old_languages.csv")
file = open(YourLocDir, 'w')
for i in NewLoc: file.write(f"{i},{NewLoc[i]}\n")
file.close()
print("Work done!")
