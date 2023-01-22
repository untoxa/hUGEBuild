# What is it

hUGEBuild is a refactoring of an original driver for hUGETracker - music module tracker, written by SuperDisk, which is intended to write misic for the game boy. The tracker itself may be found in the "releases" of this repo. Here is the original repository of the hUGETracker project: https://github.com/SuperDisk/hUGETracker It also contains a new driver, however, it is broken for now and it's new format is incompatible with this version. My goal was to put working parts of this project into one complex solution for writing and embedding music into homebrew software. Music cover used in this repo was written by Karcorp.

This refactored driver has several advantages:
1. it is modular - the driver is separated from the player and from the music data.
2. build scripts use enhanced converter utility that allows to convert RGBDS objects emitted by the RGBDS assembler into SDAS objects, that may be linked with your own GBDK-2020 project.

# How to use

1. download the hUGETracker binaries from the release: https://github.com/SuperDisk/hUGETracker/releases/latest
2. write some music module using it, export to the C source file
3. clone this repo
4. copy the exported C file into the \song\C folder of this repo
5. _make_gbdk.bat compiles the player using GBDK-2020, _make_rgbds.bat compiles the player using RGBDS; rom-files will be located in the \build folder; you must have GBDK-2020 v4.1.1 installed, in case you want to compile gbdk_player.gb.
6. for the GBDK-2020 projects it is recommended to use the library file (hUGEDriver.lib), which gets compiled into the build folder

# Notes

1. the C header file for the driver is located here: \player-gbdk\hUGEDriver.h, gbdk_player.c is the example project.
2. GBDK-2020 v4.1.1 is required. 
3. if you need to use this with GBDK-2020 project - no problem, just compile a driver into the object and convert it with rgb2sdas utility. Just add the compiled library into your project and use the functions, declared in hUGEDriver.h. Also export your song module to the C source file using hUGETracker and include it as well.

# rgb2sdas

rgb2sdas is a utility that converts RGBDS object files to SDAS object files. unfortunately, 100% complete conversion is impossible, however, utility provides sufficient subset of features to convert simple objects.

	usage: 
		rgb2sdas [-c<code_section>] [-v] [-e] [-r<symbol1>=<symbol2>] <object_name>

                -o -- output file name
		-e -- export all symbols, including local
		-r -- renames symbol symbol1 to symbol2
		-c -- codeseg area name
		-b -- default bank number for ROMX sections, -b0 forces _CODE section

	example 1; converting the driver object:
		rgb2sdas driver_lite.obj

	example 2; converting the song object, place it into bank 1, rename symbol to Intro:
		python rgb2sdas.py -c _CODE_1 -r_song_descriptor=_Intro -o song.o song.obj
