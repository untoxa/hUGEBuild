@echo off

@set PROJ=rgbds_player
@set OBJ=build\
@set SRC=player-rgbds\

@if not exist %OBJ% mkdir %OBJ%
@if exist %OBJ%%PROJ%.obj del %OBJ%%PROJ%.obj

tools\rgbasm -h -o%OBJ%%PROJ%.obj %SRC%%PROJ%.z80
