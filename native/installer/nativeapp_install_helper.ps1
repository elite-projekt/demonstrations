#nativeapp.bat has to be started first

# Script Header for prettyness
# Src: http://patorjk.com/software/taag/#p=display&h=1&v=0&c=echo&f=Mini&t=NativeApp%20Installer
Write-Host "                                      ___                             ";
Write-Host " |\ |  _. _|_ o     _   /\  ._  ._     |  ._   _ _|_  _. | |  _  ._   ";
Write-Host " | \| (_|  |_ | \/ (/_ /--\ |_) |_)   _|_ | | _>  |_ (_| | | (/_ |    ";
Write-Host "                            |   |                                     ";

# Get working directory. Should be /demonstrations/native if started from source code or should be the folder from release
$workingDirectory = Get-Location
# Check if working directory is src folder or release folder
$isReleaseDirectory = $false
if(Test-Path .env) {
    $isReleaseDirectory = $true
}
# This should also work with docker desktop
$dockerCMD = "wsl --user root docker"

function run-docker {
    param(
        [string] $param
    )
    $cmd = -join($dockerCMD, " ", $param)
    iex $cmd
    $exitcode = $LASTEXITCODE

    if ($exitcode -eq 0) {
        return $exitcode
    } else {
        # FUCK exceptions though. They are just bad design
        throw
    }
}
<#
.Synopsis
Exports environment variable from the .env file to the current process.

.Description
This function looks for .env file in the directoty of the choice, if present
it loads the environment variable mentioned in the file to the current process.

based on https://github.com/rajivharris/Set-PsEnv

.Example
 Set-PsEnv

.Example
 # This is function is called by convention in PowerShell
 # Auto exports the env variable at every prompt change
 function prompt {
     Set-PsEnv
 }
#>
#Copied from https://gist.github.com/grenzi/82e6cb8215cc47879fdf3a8a4768ec09
function Set-PsEnv {
    [CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Low')]
    param($localEnvFile = ".env")

    try {
        # return if no env file
        if (!( Test-Path $localEnvFile)) {
            Throw "could not open $localEnvFile"
    }

        # read the local env file
        $content = Get-Content $localEnvFile -ErrorAction Stop
        Write-Verbose "Parsed .env file"

        # load the content to environment
        foreach ($line in $content) {
            if ($line.StartsWith("#")) { continue };
            if ($line.Trim()) {
                $line = $line.Replace("'","")
                $kvp = $line -split "=",2
                if ($PSCmdlet.ShouldProcess("$($kvp[0])", "set value $($kvp[1])")) {
                    [Environment]::SetEnvironmentVariable($kvp[0].Trim(), $kvp[1].Trim(), "Process") | Out-Null
                }
            }
        }
    }
    catch {
        WriteOutput "Something went wrong while reading the .env file" "Red"
        Write-Warning $Error[0]
        Exit 1
    }

}

function WriteOutput {
    param(
        [string] $Message,
        [string] $Color
    )
    Write-Host "=====================================" -ForegroundColor $Color
    Write-Host $Message -ForegroundColor $Color
    Write-Host "=====================================" -ForegroundColor $Color
}

$ErrorActionPreference = "Stop"
# Check folder
$directoryPath="C:\Program Files (x86)\hda\nativeapp"
$rootCAPath="$directoryPath\demoCA\rootCA.crt"
$rootPath="C:\Program Files (x86)\hda\"
$shortcutPath ="$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\nativeapp.lnk"
$hostFile ="C:\Windows\System32\drivers\etc\hosts"

$disclaimer = @"
IMPORTANT: Please read this disclaimer carefully before installing the program.

1. Separate System or Virtual Machine Usage:
The program you are about to install is designed for experimental or testing purposes only and should never be installed or run on production systems. It is strongly advised to use a separate system or a dedicated virtual machine (VM) solely for the purpose of running this program. Installing and executing this program on production systems may lead to unpredictable outcomes, including but not limited to data loss, system instability, and security vulnerabilities.

2. Bugs and Security Related Problems:
This program is provided "as is" without any warranty or guarantee of any kind. It is important to understand that this program might contain bugs or security-related problems. The developers of this program do not assume any responsibility or liability for any damages, losses, or disruptions caused by the use of this program, including but not limited to data corruption, unauthorized access, or system compromise.

3. Experimental Nature:
This program is intended for experimental purposes and should be treated as such. It may include features, functionalities, or modifications that are still in development, untested, or subject to change without notice. By installing and using this program, you acknowledge and accept the inherent risks associated with its experimental nature.

4. Backup and Precautions:
Prior to installing the program, it is strongly recommended to perform a complete backup of all important data and system configurations. In addition, exercise caution and ensure appropriate security measures are in place to protect against potential risks associated with running experimental software.

5. Use at Your Own Risk:
Installing and using this program is entirely at your own risk. The developers and distributors of this program shall not be held responsible for any direct or indirect damages, losses, or consequences arising from its installation, execution, or use.

By proceeding with the installation, you indicate that you have read, understood, and agreed to the terms of this disclaimer. If you do not agree with any part of this disclaimer, do not proceed with the installation and remove any installed components related to this program immediately.

Type (y)es or (n)o
"@

WriteOutput "This installer will install the NativeApp" "DarkGray"

# If rootPath folder doesn't exists start install routine
If(!(Test-Path -path $rootPath)) {
    $Answer = Read-Host -Prompt $disclaimer -ErrorAction Stop
    if ($Answer -eq "y" -or $Answer -eq "yes") {
    } else {
        Exit 1
    }

    # Read env file
    if($isReleaseDirectory) {
        Set-PsEnv
    } else {
        Set-PsEnv "$workingDirectory\..\..\.env"
    }

    try {
        WriteOutput "Trying to create the folder path: $rootPath" "DarkGray"
        $null = New-Item -Path $rootPath -ItemType directory -ErrorAction Stop
        WriteOutput "Folder path has been created successfully at: $rootPath" "Green"
    } catch {
        WriteOutput "Something went wrong while creating the folder path: $rootPath" "Red"
        Write-Warning $Error[0]
        Exit 1
    }

    $objUser = New-Object System.Security.Principal.NTAccount(whoami)

    # Setting directory security
    try {
        WriteOutput "Trying to set directory security" "DarkGray"
        $colRights = [System.Security.AccessControl.FileSystemRights]"Modify"
        $inheritanceFlag = [System.Security.AccessControl.InheritanceFlags]"ContainerInherit, ObjectInherit"
        $propagationFlag = [System.Security.AccessControl.PropagationFlags]::None
        $objType =[System.Security.AccessControl.AccessControlType]::Allow
        $objACE = New-Object System.Security.AccessControl.FileSystemAccessRule($objUser, $colRights, $inheritanceFlag, $propagationFlag, $objType)
        $objACL = Get-Acl -Path $rootPath
        $objACL.AddAccessRule($objACE)
        Set-ACL $rootPath $objACL -ErrorAction Stop
        WriteOutput "Set directory security" "Green"
    }
    catch {
        WriteOutput "Something went wrong while setting directory security" "Red"
        Write-Warning $Error[0]
        WriteOutput "Resetting all changes" "Red"
        Remove-Item -Path $rootPath -Recurse
        Exit 1
    }

    try {
        WriteOutput "Trying to create the folder path: $directoryPath" "DarkGray"
        $null = New-Item -ItemType Directory -Path $directoryPath -ErrorAction Stop
        WriteOutput "Folder path has been created successfully at: $directoryPath" "Green"
    } catch {
        WriteOutput "Something went wrong while creating the folder path: $directoryPath" "Red"
        Write-Warning $Error[0]
        WriteOutput "Resetting all changes" "Red"
        Remove-Item -Path $rootPath -Recurse
        Exit 1
    }

    # Copy data
    try {
        WriteOutput "Trying to copy files to the created folder" "DarkGray"
        Copy-Item "$workingDirectory/../../*" -Destination "$directoryPath/" -Recurse -Force -ErrorAction Stop
        WriteOutput "Copied files to the created folder" "Green"
    }
    catch {
        WriteOutput "Something went wrong while copying file to the folder paths" "Red"
        Write-Warning $Error[0]
        WriteOutput "Resetting all changes" "Red"
        Remove-Item -Path $rootPath -Recurse
        Exit 1
    }

    # Host File DEPRECATED! Use Admin component instead
    $localRedirects = "127.0.0.1`twww.lieferung-amazon.de www.shipment-support-amazon.com covidsupportgermany.de coronahilfengermany.de mpseinternational.com mail.domain.com de.linkedln.com #MPSE"
    try {
        $containsRedirecets = Select-String -Path $hostFile -Pattern '#MPSE' -ErrorAction Stop
        if($containsRedirecets -ne $null) {
            WriteOutput "Updating 127.0.0.1 entry" "DarkGray"
            $line = Get-Content $hostFile | Select-String '#MPSE' | Select-Object -ExpandProperty Line -ErrorAction Stop
            $content = Get-Content $hostFile -ErrorAction Stop
            $content | ForEach-Object {$_ -replace $line, $localRedirects} | Set-Content $hostFile -ErrorAction Stop
        } else {
            WriteOutput "Write redirects to end of hosts-file" "DarkGray"
            Add-Content -Path $hostFile -Value "`n$localRedirects" -ErrorAction Stop
        }
        WriteOutput "Edited succesfully host file" "Green"
    } catch {
        WriteOutput "Something went wrong while writing into hostfile" "Red"
        Write-Warning $Error[0]
        WriteOutput "Resetting all changes" "Red"
        Remove-Item -Path $rootPath -Recurse
        Exit 1
    }

    # Set Windows Defender Exception
    try {
        WriteOutput "Trying to add exclusion in Windows Defender for native app" "DarkGray"
        Add-MpPreference -ExclusionPath $rootPath -ErrorAction Stop
        WriteOutput "Added Exclusion in Windows Defender for native app" "Green"
    } catch {
        WriteOutput "Something went wrong while setting the exclusions for Windows Defender" "Red"
        Write-Warning $Error[0]
        WriteOutput "Resetting all changes" "Red"
        Remove-Item -Path $rootPath -Recurse
        Set-Content -Path $hostFile -Value (get-content -Path $hostFile | Select-String -Pattern '#MPSE' -NotMatch)
        Exit 1
    }

    # Install nativeapp from wheel
    try {
        WriteOutput "Trying to install native app from build wheel" "DarkGray"
        python -m venv $directoryPath/.venv
        . $directoryPath/.venv/Scripts/Activate.ps1
        pip install -I $directoryPath
        # FIXME: When only running it once the .mo files are missing on Windows. No clue why
        pip install -I $directoryPath
        WriteOutput "Installed nativeapp into venv" "Green"
    } catch {
        WriteOutput "Something went wrong while installing native app from wheel" "Red"
        Write-Warning $Error[0]
        WriteOutput "Resetting all changes" "Red"
        Remove-Item -Path $rootPath -Recurse
        Set-Content -Path $hostFile -Value (get-content -Path $hostFile | Select-String -Pattern '#MPSE' -NotMatch)
        Exit 1
    }


    # Information
    Write-Host -ForegroundColor DarkGray "====================================="
    Write-Host -ForegroundColor DarkGray "Information"
    Write-Host -ForegroundColor DarkGray "To cover all dependencies please do the following:"
    Write-Host -ForegroundColor DarkGray " - Have Docker for windows with the Linux subsystem installed"
    Write-Host -ForegroundColor DarkGray " - Install the Thunderbird mail client on the system"
    Write-Host -ForegroundColor DarkGray " - Import the 'rootCA.crt' certificate (provided via the program folder) into the browser of your choice - [trust identifying websites]"
    Write-Host -ForegroundColor DarkGray " - pull the latest images for the demos if the script not succeded`n"
    Write-Host -ForegroundColor DarkGray "====================================="
    # Pull docker images
    try {
        WriteOutput "Login with your username and password for the $Env:REGISTRY_URL repository" "DarkGray"
        # run-docker "login --username WorkstationToken  --password SAHRbswUazao1W_EyuYW $Env:REGISTRY_URL"
        # For Pulling Images from Repo
        # WriteOutput "Trying to pull the latest docker images" "DarkGray"
        # run-docker "pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:FOKUSRNWARE_REPO"
        # run-docker "pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:RANSOMWARE_REPO"
        # run-docker "pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:UHH_DUCKY_MITM_REPO_WEB"
        # run-docker "pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:UHH_DUCKY_MITM_REPO_WEB_EN"
        # run-docker "pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:UHH_DUCKY_MITM_REPO_PROXY"
        # run-docker "pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:PHISHING_REPO"
        # run-docker "pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:HDA_PASSWORD_REPO"
        # run-docker "pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:HDA_PASSWORD_NGINX_REPO"
        # WriteOutput "Succesfully pulled the docker images" "Green"
        run-docker "pull mailserver/docker-mailserver"

        # when building locally just login successfully"
        WriteOutput "Successfully logged in" "Green"
    } catch {
        # For Pulling Images from Repo
         WriteOutput "Something went wrong while login into docker or pulling the repositories" "Red"
         Write-Warning $Error[0]
         WriteOutput "Resetting all changes" "Red"
         Remove-Item -Path $rootPath -Recurse
         Remove-MpPreference -ExclusionPath $rootPath
         Exit 1
    }

    #Build images locally
    try {
        WriteOutput "Building Images locally" "DarkGray"
        wsl --user root ../../build_images.py
    } catch {
        WriteOutput "Something went wrong while building the images locally" "Red"
        Write-Warning $Error[0]
        Exit 1
    }

    # Create Shortcut and autostart entry
    try {
        WriteOutput "Try to create a new autostart entry" "DarkGray"
        #XXX: It works but Windows adds some error. It works and I can't be bothered to decode Windows' shitty Powershell syntax!
        $action = New-ScheduledTaskAction -Execute "powershell " -Argument "-Windowstyle hidden ./.venv/Scripts/nativeapp.exe -p . *> nativeapp_main.log" -WorkingDirectory "$directoryPath"
        $trigger = New-ScheduledTaskTrigger -AtLogon
        $principal = New-ScheduledTaskPrincipal -UserId $(whoami) -RunLevel Limited
        $settings = New-ScheduledTaskSettingsSet
        $task = New-ScheduledTask -Action $action -Principal $principal -Trigger $trigger -Settings $settings
        Register-ScheduledTask "ELITE nativeapp" -InputObject $task

        $action_admin = New-ScheduledTaskAction -Execute "powershell " -Argument "-Windowstyle hidden ./.venv/Scripts/python.exe -m nativeapp.utils.admin.admin_app --mode server" -WorkingDirectory "$directoryPath"
        $principal_admin = New-ScheduledTaskPrincipal -UserId $(whoami) -RunLevel Highest
        $task_admin = New-ScheduledTask -Action $action_admin -Principal $principal_admin -Trigger $trigger -Settings $settings
        Register-ScheduledTask "ELITE nativeapp admin" -InputObject $task_admin

        WriteOutput "Created an autostart entry" "Green"
    }
    catch {
        WriteOutput "Something went wrong creating the autostart entry" "Red"
        Write-Warning $Error[0]
        WriteOutput "Resetting all changes" "Red"
        Remove-Item -Path $rootPath -Recurse
        Set-Content -Path $hostFile -Value (get-content -Path $hostFile | Select-String -Pattern '#MPSE' -NotMatch)
        Remove-MpPreference -ExclusionPath $rootPath
        Unregister-ScheduledTask -TaskName "ELITE nativeapp"
        Unregister-ScheduledTask -TaskName "ELITE nativeapp admin"
        Exit 1
    }

    try {
        Import-Certificate -FilePath $rootCAPath -CertStoreLocation Cert:\LocalMachine\Root
    }
    catch{
        WriteOutput "Something went wrong while adding rootCa" "Red"
        Write-Warning $Error[0]
    }

    # Finisch message
    WriteOutput "The installation was succesfully" "Green"

# If rootPath folder exists uninstall routine
} Else {
    WriteOutput "The given folder path $directoryPath already exists" "DarkGray"
    try {
        $Answer = Read-Host -Prompt "Do you really want to uninstall the native app? `n Type (y)es or (n)o" -ErrorAction Stop
        if ($Answer -eq "y" -or $Answer -eq "yes") {
            WriteOutput "Trying to uninstall" "DarkGray"

            try {
                # Kill process if exists
                WriteOutput "Trying to kill the nativeapp process if exists" "DarkGray"
                Stop-ScheduledTask -TaskName "ELITE nativeapp"
                Stop-ScheduledTask -TaskName "ELITE nativeapp admin"
            }
            catch {
                WriteOutput "Something went wrong while killing the native app process" "Red"
                Write-Warning $Error[0]
            }

            try {
                # Remove folder
                WriteOutput "Trying to remove the folder: $rootPath" "DarkGray"
                Remove-Item -Path $rootPath -Recurse -Force -ErrorAction Stop
                WriteOutput "Removed the folder with all files: $rootPath" "Green"
            }
            catch {
                WriteOutput "Something went wrong while removing the folder: $rootPath" "Red"
                Write-Warning $Error[0]
            }

            try {
                # Remove Windows Defender Exception
                WriteOutput "Trying to remove the exclusion from Windows Defender" "DarkGray"
                Remove-MpPreference -ExclusionPath $rootPath -ErrorAction Stop
                WriteOutput "Removed the exclusion from Windows Defender" "Green"
            }
            catch {
                WriteOutput "Something went wrong removing the exclusion from Windows Defender" "Red"
                Write-Warning $Error[0]
            }

              try {
                # Remove task
                WriteOutput "Trying to remove the task entry" "DarkGray"
                Unregister-ScheduledTask -TaskName "ELITE nativeapp"
                Unregister-ScheduledTask -TaskName "ELITE nativeapp admin"
                WriteOutput "Removed the task entry" "Green"
            }
            catch {
                WriteOutput "Something went wrong while removing the task entry" "Red"
                Write-Warning $Error[0]
            }

            try {
                # Remove Host entry
                WriteOutput "Removing host entry" "DarkGray"
                Set-Content -Path $hostFile -Value (get-content -Path $hostFile | Select-String -Pattern '#MPSE' -NotMatch) -ErrorAction Stop
                WriteOutput "Removed successfully host entry" "Green"
            }
            catch {
                WriteOutput "Something went wrong while removing hosts entry" "Red"
                Write-Warning $Error[0]
            }
        }
    }
    catch {
        WriteOutput "Something went wrong while uninstalling the native app" "Red"
        Write-Warning $Error[0]
        Exit 1
    }

    # Uninstall message
    WriteOutput "The uninstall was succefully" "Green"
}

try {
    Write-Host "Press any key to continue..."
    $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    Stop-process -Id $PID
}
catch {
    WriteOutput "Please type a key to exit this script" "Red"
    Write-Warning $Error[0]
    Exit 1
}
