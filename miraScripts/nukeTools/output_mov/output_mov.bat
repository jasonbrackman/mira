@echo off
cd /d %~dp0
for %%i in (%*) do python ./do_output_mov.py %%i
pause