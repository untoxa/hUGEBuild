@echo off
@set PROJ=gbdk_player
@set GBDK=..\..\gbdk\
@set GBDKLIB=%GBDK%lib\small\asxxxx\
@set OBJ=build
@set SRC=player-gbdk
@set TGT=rom

@set DRV=hUGEDriver
@set MOD=song

@set CVTFLAGS=-b0

@echo Cleanup...

@if exist %TGT%/%PROJ%.gb del %TGT%/%PROJ%.gb
@if exist %TGT%/%PROJ%.sym del %TGT%/%PROJ%.map
@if exist %TGT%/%PROJ%.sym del %TGT%/%PROJ%.ihx
@if exist %TGT%/%PROJ%.map del %TGT%/%PROJ%.noi

@if not exist %OBJ% mkdir %OBJ%
@if not exist %TGT% mkdir %TGT%

@echo Assembling song and driver...

tools\rgbasm -DGBDK -o%OBJ%/%DRV%.obj hUGEDriver.asm
tools\rgb2sdas %CVTFLAGS% %OBJ%\%DRV%.obj
%GBDK%\bin\sdar q %OBJ%\hUGEDriver.lib %OBJ%\%DRV%.obj.o

@echo COMPILING WITH GBDK-2020...

%GBDK%\bin\lcc -I%SRC% -Wl-m -Wl-w -Wl-j -Wm-yS -Wl-k%OBJ% -Wl-lhUGEDriver.lib -o %TGT%/%PROJ%.gb %SRC%/%PROJ%.c song/C/%MOD%.c

@echo DONE!
