@echo off
@set PROJ=gbdk_player
@set GBDK=..\..\gbdk\
@set GBDKLIB=%GBDK%lib\small\asxxxx\
@set OBJ=build\
@set SRC=player-gbdk\
@set TGT=rom\

@set DRV=driver_lite
@set MOD=song
@rem @set CVTFLAGS=-e

@echo Cleanup...

@if exist %TGT%%PROJ%.gb del %TGT%%PROJ%.gb
@if exist %TGT%%PROJ%.sym del %TGT%%PROJ%.map
@if exist %TGT%%PROJ%.sym del %TGT%%PROJ%.ihx
@if exist %TGT%%PROJ%.map del %TGT%%PROJ%.noi

@if not exist %OBJ% mkdir %OBJ%
@if not exist %TGT% mkdir %TGT%

@echo Assembling song and driver...

tools\rgbasm -o%OBJ%%DRV%.obj %DRV%.z80
tools\rgb2sdas %CVTFLAGS% %OBJ%%DRV%.obj
@set LFILES=%LFILES% %OBJ%%DRV%.obj.o

tools\rgbasm -i%MOD% -o%OBJ%%MOD%.obj %MOD%.z80
tools\rgb2sdas %CVTFLAGS% -b1 -r_song_descriptor=_Intro %OBJ%%MOD%.obj
@set LFILES=%LFILES% %OBJ%%MOD%.obj.o

@echo COMPILING WITH GBDK-2020...

%GBDK%\bin\lcc -o %TGT%%PROJ%.gb %SRC%%PROJ%.c %LFILES%

@echo DONE!
