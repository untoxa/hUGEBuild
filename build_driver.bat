@echo off

@set PROJ=driver_lite
@set OBJ=build\

@if not exist %OBJ% mkdir %OBJ%
@if exist %OBJ%%PROJ%.obj del %OBJ%%PROJ%.obj

tools\rgbasm -E -h -o%OBJ%%PROJ%.obj %PROJ%.z80