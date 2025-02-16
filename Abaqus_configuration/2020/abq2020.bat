call "C:\Program Files (x86)\Intel\oneAPI\setvars.bat" -arch intel64
call "C:\Program Files (x86)\Intel\oneAPI\setvars-vcvarsall.bat" -arch intel64
@echo off
rem setlocal
rem set ABA_COMMAND=%~nx0
rem set ABA_COMMAND_FULL=%~f0
@call
"C:\SIMULIA\EstProducts\2020\win_b64\code\bin\ABQLauncher.exe" %*
rem endlocal