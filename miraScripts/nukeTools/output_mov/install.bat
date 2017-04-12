@echo off
reg add HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\shell\convert_to_mov\command /ve /t REG_SZ /d "C:/tools/Nuke9.0v3/python.exe Z:/Resource/Support/aas_repos/aas_scripts/aas_nukeTools/output_mov/do_output_mov.py %%1"
pause