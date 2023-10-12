# navalart localization combiner

## this script may break your localization file, all you need to fix it - delete \<feff> on the start of some lines

this script combines all official localization files into one and then replaces values from the mod, so it easier to work on localization mods after game update.

this works only on linux, but if you comment 2 lines of the code (#!/bin/python3 and system(f"mv ... ...")) it should work on windows too.
