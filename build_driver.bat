@echo off

@set PROJ=driver
@set OBJ=build\

@if not exist %OBJ% mkdir %OBJ%
@if exist %OBJ%%PROJ%.obj del %OBJ%%PROJ%.obj

tools\rgbasm -E -h -o%OBJ%hUGEDriver.obj %PROJ%.z80