@echo off
cd /d %~dp0
for %%i in (%*) do C:/tools/Nuke9.0v3/python.exe ./do_output_mov.py %%i
pause