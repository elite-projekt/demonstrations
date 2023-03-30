@echo off

:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"


set powershellScriptFileName=nativeapp_install_helper.ps1

start /b wsl --user root dockerd


@setlocal enableextensions
@cd /d "%~dp0"
set dir_name=%cd%
powershell -Command "Add-MpPreference -ExclusionPath '%dir_name%'"
powershell -Command "cd '%dir_name%'; Expand-Archive -Force -Path elite.zip -DestinationPath .\elite"
cd %dir_name%\elite\native\installer
Powershell.exe -executionpolicy Bypass -File %powershellScriptFileName%
cd %dir_name%
powershell -Command "cd '%dir_name%'; Remove-Item -Recurse 'elite'"
powershell -Command "Remove-MpPreference -ExclusionPath '%dir_name%'"
pause
