@echo off

set scriptFileName=%~n0
set scriptFolderPath=%~dp0
set powershellScriptFileName=install_dependencies.ps1

powershell -Command "Start-Process powershell \"-ExecutionPolicy Bypass -NoProfile -NoExit -Command `\"cd \`\"%scriptFolderPath%`\"; & \`\".\%powershellScriptFileName%\`\"`\"\" -Verb RunAs"
