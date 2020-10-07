@echo off
@set PROJ=gbdk_player
@set GBDK=..\..\gbdk\
@set GBDKLIB=%GBDK%lib\small\asxxxx\
@set OBJ=build\
@set SRC=player-gbdk\
@set TGT=rom\

@set DRV=hUGEDriver
@set MOD=song

@echo Cleanup...

@if exist %TGT%%PROJ%.gb del %TGT%%PROJ%.gb
@if exist %TGT%%PROJ%.sym del %TGT%%PROJ%.map
@if exist %TGT%%PROJ%.sym del %TGT%%PROJ%.ihx
@if exist %TGT%%PROJ%.map del %TGT%%PROJ%.noi

@if not exist %OBJ% mkdir %OBJ%
@if not exist %TGT% mkdir %TGT%

@echo Assembling song and driver...

tools\rgbasm -o%OBJ%%DRV%.obj driver.z80
tools\rgb2sdas %CVTFLAGS% %OBJ%%DRV%.obj
@set LFILES=%LFILES% %OBJ%%DRV%.obj.o

@echo COMPILING WITH GBDK-2020...

%GBDK%\bin\lcc -I%SRC% -Wl-m -Wl-w -Wl-j -o %TGT%%PROJ%.gb %SRC%%PROJ%.c song/C/%MOD%.c %LFILES%

@echo DONE!
