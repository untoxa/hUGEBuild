@echo off
@set PROJ=gbdk_player
@set GBDK=..\..\gbdk\
@set GBDKLIB=%GBDK%lib\small\asxxxx\
@set OBJ=build\
@set SRC=player-gbdk\
@set TGT=rom\

@set CFLAGS=-mgbz80 --fsigned-char --no-std-crt0 -I %GBDK%include -I %GBDK%include\asm -I %SRC%include -c
@set CFLAGS=%CFLAGS% --max-allocs-per-node 50000

@set LNAMES=-g .OAM=0xC000 -g .STACK=0xE000 -g .refresh_OAM=0xFF80 -b _DATA=0xc0a0 -b _CODE=0x0200
@set LFLAGS=-n -m -w -j -i -k %GBDKLIB%gbz80\ -l gbz80.lib -k %GBDKLIB%gb\ -l gb.lib %LNAMES%
@set CRT0=%GBDKLIB%gb\crt0.o

@rem @set CVTFLAGS=-e
@set BINFLAGS=-yt 1 -yo 4

@set ASMFLAGS=-plosgff -I%GBDKLIB%

@echo Cleanup...

@if exist %TGT%%PROJ%.gb del %TGT%%PROJ%.gb
@if exist %TGT%%PROJ%.sym del %TGT%%PROJ%.map
@if exist %TGT%%PROJ%.sym del %TGT%%PROJ%.ihx
@if exist %TGT%%PROJ%.map del %TGT%%PROJ%.noi

@if not exist %OBJ% mkdir %OBJ%
@if not exist %TGT% mkdir %TGT%

@echo Assemble song and driver...

@set DRV=driver_lite
tools\rgbasm -o%OBJ%%DRV%.obj %DRV%.z80
tools\rgb2sdas %CVTFLAGS% %OBJ%%DRV%.obj
@set LFILES=%LFILES% %OBJ%%DRV%.obj.o

@set MOD=song
tools\rgbasm -i%MOD% -o%OBJ%%MOD%.obj %MOD%.z80
tools\rgb2sdas %CVTFLAGS% -c_CODE_1 -r_song_descriptor=_Intro %OBJ%%MOD%.obj
@set LFILES=%LFILES% %OBJ%%MOD%.obj.o


@echo COMPILING WITH SDCC4...

sdcc %CFLAGS% %SRC%%PROJ%.c -o %OBJ%%PROJ%.rel

@echo LINKING...
sdldgb %LFLAGS% %TGT%%PROJ%.ihx %CRT0% %OBJ%%PROJ%.rel %LFILES% 

@echo MAKING BIN...
makebin -Z %BINFLAGS% %TGT%%PROJ%.ihx %TGT%%PROJ%.gb

@echo DONE!
