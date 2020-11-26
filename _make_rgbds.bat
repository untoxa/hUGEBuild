@echo off

@set OBJ=build\
@set PROJ=rgbds_player
@set SONG=song
@set TGT=rom\

@if not exist %OBJ% mkdir %OBJ%
@if exist %OBJ%hUGEDriver.obj del %OBJ%hUGEDriver.obj
@if exist %OBJ%%SONG%.obj del %OBJ%%SONG%.obj
@if exist %OBJ%%PROJ%.obj del %OBJ%%PROJ%.obj
@if not exist %TGT% mkdir %TGT%

tools\rgbasm -E -h -o%OBJ%hUGEDriver.obj hUGEDriver.asm
tools\rgbasm -isong/asm/%SONG% -o%OBJ%%SONG%.obj song.asm
tools\rgbasm -h -o%OBJ%%PROJ%.obj player-rgbds\%PROJ%.asm

tools\rgblink -n%TGT%%PROJ%.sym -o%TGT%%PROJ%.gb %OBJ%%PROJ%.obj %OBJ%hUGEDriver.obj %OBJ%%SONG%.obj

tools\rgbfix -p0 -v %TGT%%PROJ%.gb
 