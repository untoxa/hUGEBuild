@echo off

@set OBJ=build\
@set TGT=rom\

@if exist %OBJ% rd /s/q %OBJ%
@if exist %TGT% rd /s/q %TGT%
