@echo off
echo PYTHONPATH��������
set regpath=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
set evname=PYTHONPATH
set pythonpath=Z:\env;Z:\mira;
reg add "%regpath%" /v %evname% /d %pythonpath% /f
