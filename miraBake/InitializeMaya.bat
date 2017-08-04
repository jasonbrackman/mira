@echo off
set source_maya_env_path=Z:\mira\Maya.env
set user_maya_env_dir=%USERPROFILE%\Documents\maya\2016
set destin_maya_env_path=%user_maya_env_dir%\Maya.env
set source_tools_path=Z:\mira_tools
set destin_tools_path=C:\tools\mira_tools

rem copy Maya.env
if exist %source_maya_env_path% (
	if not exist %user_maya_env_dir% md %user_maya_env_dir%
	copy %source_maya_env_path% %destin_maya_env_path%
) else (
	echo %source_maya_env_path% does not exist.
)


rem copy mira_tools
if exist %source_tools_path% ( 
	goto copy_tools
) else (
	echo %source_tools_path% does not exist.
)

:copy_tools
if not exist %destin_tools_path% md %destin_tools_path%
xcopy %source_tools_path% %destin_tools_path% /y /s /e /f
if %errorlevel% equ 0 (
    echo 拷贝文件成功
) else (
echo 拷贝文件失败
)

echo done
pause
