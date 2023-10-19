#!/bin/python3
from sys     import argv
from os.path import exists
from csv     import reader, writer
from pathlib import Path

#varibles
force = False
helptext = "\ncombiner\n - combines all localisation files and your localisation file into new localisation file. \nCreated by @tunguso4ka. \nArgv commands - 'help', 'force', 'GameLocDir=path', 'YourLocDir=path'"

#loading pathes from config
file = open('config')
lines = file.readlines()
GameLocDir = lines[0].strip()
YourLocDir = lines[1].strip()
file.close()
print("Config loaded.")

#reading argv
for i in argv[1:]:
    f = i.split('=', 1)
    if f[0] == 'GameLocDir': GameLocDir = f[1]
    elif f[0] == 'YourLocDir': YourLocDir = f[1]
    elif f[0] == 'force': force = True
    elif f[0] == 'help': print(helptext); exit()

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
            if doformat: LocList[i[0]] = i[2].strip()
            else: LocList[i[0]] = i[1].strip()
        return LocList

#combining official game locals into one
#aircraftweapons.csv, parts.csv, mission.csv, tips.csv, tutorials.csv, aircraftweaponsDes.csv, descriptions.csv, languages.csv
for i in ["languages.csv", "tips.csv", "tutorials.csv", "parts.csv", "descriptions.csv", "aircraftweapons.csv", "aircraftweaponsDes.csv"]:
    if not exists(GameLocDir+i): print(f"Directory {i} does not exist. Skipping..."); continue
    GameLoc |= ReturnLocList(GameLocDir+i, True)
print(f"Loaded {len(GameLoc)} game localization lines.")

#getting your local
if exists(YourLocDir+"languages.csv"):
    YourLoc |= ReturnLocList(YourLocDir+"languages.csv")
    print(f"Loaded {len(YourLoc)} your localization lines.")

#combining both locals
NewLoc = GameLoc | YourLoc
print(f"Combined into {len(NewLoc)} new localization lines.")

#safety feature (WOW!)
if not force:
    res = input("Proceed? y/N - ")
    if res not in "yY": exit()

#moving old local file and creating a new one from combined localization
if exists(YourLocDir+"languages.csv"): Path(YourLocDir+"languages.csv").rename(YourLocDir+"old_languages.csv")

file = open(YourLocDir+"languages.csv", 'w')
for i in NewLoc: file.write(f"{i},{NewLoc[i]}\n")
file.close()
print("Work done!")
