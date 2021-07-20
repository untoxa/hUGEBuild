# What is it

hUGEBuild is a refactoring of an original driver for hUGEReacker - music module tracker written by SuperDisk which is intended to write misic for the game boy. The tracker itself may be found in the "releases" of this repo. Here is an original repository of hUGETracker: https://github.com/SuperDisk/hUGETracker It also contains a new driver, however, it is broken for now and it's new format is incompatible with this version. My goal was to put working parts of this project into one complex solution for writing and embedding music into homebrew software. Music cover used in this repo was written by Karcorp.

This refactored driver has several advantages:
1. it is modular - the driver is separated from the player and from the music data.
2. build scripts use enhanced converter utility that allows to converting RGBDS objects created by RGBDS assembler into SDAS objects, that might be linked with your own GBDK-powered project.

# How to use

1. download hUGETracker binaries from the release: https://github.com/SuperDisk/hUGETracker/releases/latest
2. write a music modute in it, export to C source file
3. clone this repo
4. copy exported C file into the \song\C folder of this repo
5. _make_gbdk.bat compiles a player using GBDK-2020, _make_rgbds.bat compiles a player using RGBDS; rom-files will be located in the \rom folder; you must have more GBDK-2020 v4.0, in case you want to compile gbdk_player.gb, because bat-scripts are written for it.
6. objects that might be linked with your homebrew software are located in the \build folder: hUGEDriver.obj song.obj in RGBDS format, hUGEDriver.obj.o in SDAS format for use with GBDK.

# Notes

1. C header file for the driver is here: \player-gbdk\hUGEDriver.h, example of usage is gbdk_player.c
2. GBDK-2020 v4.0 is required. 
3. If you need to use this with GBDK-2020 project - no problem, just compile a driver into the object and convert it with rgb2sdas utility. Just add converted object to your project and use functions declared in hUGEDriver.h in your homebrew. Also export your song module to C source file using hUGETracker and include it too.

# rgb2sdas

rgb2sdas is a utility that converts RGBDS object files to SDAS object files. unfortunately, 100% complete conversion is impossible, however, utility provides sufficient subset of features to convert simple objects.

	usage: 
		rgb2sdas [-c<code_section>] [-v] [-e] [-r<symbol1>=<symbol2>] <object_name>

		-v -- verbous output, outputs debug information
		-e -- export all symbols, including local
		-r -- renames symbol symbol1 to symbol2
		-c -- codeseg area name
		-b -- default bank number for ROMX sections, -b0 forces _CODE section

	example 1; converting the driver object:
		rgb2sdas driver_lite.obj

	example 2; converting the song object, place it into bank 1, rename symbol to Intro:
		rgb2sdas -c_CODE_1 -r_song_descriptor=_Intro song.obj
