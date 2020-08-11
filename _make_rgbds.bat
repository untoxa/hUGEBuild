@echo off

@set OBJ=build\
@set TGT=rom\

call build_driver.bat
call build_song.bat

call build_player.bat
call link.bat 