@echo off

@set PROJ=song
@set OBJ=build\

@if not exist %OBJ% mkdir %OBJ%
@if exist %OBJ%%PROJ%.obj del %OBJ%%PROJ%.obj

tools\rgbasm -o%OBJ%%PROJ%.obj %PROJ%.z80
