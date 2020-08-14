# What is it

hUGEBuild is a refactoring of an original driver for hUGEReacker - music module tracker for game boy. The tracker itself may be found in the "releases" of this repo. Here is an original repository of hUGETracker: https://github.com/SuperDisk/hUGETracker It also contains a new driver, however, it is broken for now and it's new format is incompatible with this version. My goal was to put working parts of this project into one complex solution for writing and embedding music into homebrew software.

This refactored driver has several advantages:
1. it is modular - the driver is separated from the player and from the music data.
2. build scripts use enhanced converter utility that allows to converting RGBDS objects created by RGBDS assembler into SDAS objects, that might be linked with your own GBDK-powered project.

# How to use

1. download hUGETracker binaries from the release: https://github.com/untoxa/hUGEBuild/releases/latest
2. write a music modute in it, press "export .GB" button
3. clone this repo
4. copy *.htt files from hUGETracker\hUGEDriver\ folder to \song folder of this repo
5. _make_gbdk.bat compiles a player using SDCC, _make_rgbds.bat compiles a player using RGBDS; rom-files will be located in the \rom folder; you must have more or less new SDCC, in case you want to compile gbdk_player.gb, because bat-scripts are written for it.
6. objects that might be linked with your homebrew software are located in the \build folder: driver_lite.obj song.obj in RGBDS format, driver_lite.obj.o song.obj.o in SDAS format for use with SDCC.

# Notes

1. SDCC header file for the driver is here: \player-gbdk\hUGEDriver.h, example of usage is gbdk_player.c
2. New SDCC must be used, at least #11800. I suggest to take snapshot from here: http://sdcc.sourceforge.net/snap.php You may take GBDK-2020 library to link with. 
3. If you need to use this with pure GBDK-2020 - no problem, just compile a song and a driver into objects and convert them with rgb2sdas utility. Just add converted objects to your project and use functions declared in hUGEDriver.h in your homebrew.

# todo

1. try to bring hUGETracker original project to life: it has a newer driver, with more functions, also a better UI, but is completely unusable because it is simply not working when compiled from the sources, and there are no more or less stable pre-compiled binaries of it to use.
