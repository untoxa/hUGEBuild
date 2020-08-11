@echo off

@echo off

@set PROJ=rgbds_player
@set OBJ=build\
@set TGT=rom\

@if not exist %TGT% mkdir %TGT%

tools\rgblink -m%TGT%%PROJ%.map -n%TGT%%PROJ%.sym -o%TGT%%PROJ%.gb %OBJ%%PROJ%.obj %OBJ%driver_lite.obj %OBJ%song.obj
tools\rgbfix -p0 -v %TGT%%PROJ%.gb