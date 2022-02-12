# WMO-to-WDT
Generates a WDT for your WMO only maps from the WMO file.

What is it for ?
- Some WoW maps (usualy dungeons) are "WMO only", they don't have any map tiles (.adt), and instead only render a WMO model referenced in the .wdt file. This tool allows to create a WDT file and properly fills its data from your WMO, mostly the boundings info, and seting the flag to use WMO definition.

Requirements :
- Python 3

How to use : 
- This is a drag and drop tool, to use, simply drop your WMO root file onto this WMO to WDT.py script.
- Then just drop the .wdt in your map folder defined in Map.dbc, rename your .wdt to the map's name if needed(it just uses the model name by default).

It has only been tested for WOTLK and older, not guarenteed to work with recent WoW versions.
