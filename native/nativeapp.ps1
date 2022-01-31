#nativeapp.bat has to be started first

Write-Host "                                      ___                           ";
Write-Host " |\ |  _. _|_ o     _   /\  ._  ._     |  ._   _ _|_  _. | |  _  ._ ";
Write-Host " | \| (_|  |_ | \/ (/_ /--\ |_) |_)   _|_ | | _>  |_ (_| | | (/_ |  ";
Write-Host "                            |   |                                   ";

# Get working directory. Should be /demonstrations/native if started from source code or should be the folder from release
$workingDirectory = Get-Location
# Check if working directory is src folder or release folder
$isReleaseDirectory = $false
if(Test-Path .env) {
    $isReleaseDirectory = $true   
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
$rootPath="C:\Program Files (x86)\hda\"
$shortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\nativeapp.lnk"
$hostFile = "C:\Windows\System32\drivers\etc\hosts"

If(!(Test-Path -path $rootPath)) {
    try {
        WriteOutput "Trying to create the folder path: $rootPath" "DarkGray"
        $null = New-Item -Path $rootPath -ItemType directory -ErrorAction Stop
        WriteOutput "Folder path has been created successfully at: $rootPath" "Green"
    } catch {
        WriteOutput "Something went wrong while creating the folder path: $rootPath" "Red"
        Write-Warning $Error[0]
        Exit 1
    }
    
    # Check system language
    $lang = [CultureInfo]::InstalledUICulture
    if($lang -eq "de-DE") {
        $objUser = New-Object System.Security.Principal.NTAccount("VORDEFINIERT\Benutzer")
    } else {
        $objUser = New-Object System.Security.Principal.NTAccount("BUILTIN\USER")
    }

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
        WriteOutput "Trying to copie files to the created folder" "DarkGray"
        if($isReleaseDirectory) {
            Copy-Item ".env" -Destination $directoryPath -ErrorAction Stop
            Copy-Item "stacks\" -Destination "$directoryPath\stacks" -Recurse -Force -ErrorAction Stop
            Copy-Item "rootCA.crt" -Destination "$directoryPath\stacks" -ErrorAction Stop
            Copy-Item "profiles" -Destination "$directoryPath" -Recurse -ErrorAction Stop
            Copy-Item "app.exe" -Destination "$directoryPath" -ErrorAction Stop
        } else {
            Copy-Item "$workingDirectory\..\.env" -Destination $directoryPath -ErrorAction Stop
            Copy-Item "$workingDirectory\stacks\" -Destination "$directoryPath\stacks" -Recurse -Force -ErrorAction Stop
            Copy-Item "$workingDirectory\..\demoCA\rootCA.crt" -Destination "$directoryPath\stacks" -ErrorAction Stop
            Copy-Item "$workingDirectory\src\profiles" -Destination "$directoryPath" -Recurse -ErrorAction Stop
            Copy-Item "$workingDirectory\src\dist\windows\app.exe" -Destination "$directoryPath"  -ErrorAction Stop
        }
        WriteOutput "Copied files to the created folder" "Green"
    }
    catch {
        WriteOutput "Something went wrong while copying file to the folder paths" "Red"
        Write-Warning $Error[0]
        WriteOutput "Resetting all changes" "Red"
        Remove-Item -Path $rootPath -Recurse
        Exit 1
    }
    
    # Host File
    $localRedirects = "127.0.0.1`twww.shipment-support-amazon.com covidsupportgermany.de coronahilfengermany.de mpseinternational.com mail.domain.com #MPSE"
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

    if($isReleaseDirectory) {
        Set-PsEnv
    } else {
        Set-PsEnv "$workingDirectory\..\.env"
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
        docker login $Env:REGISTRY_URL 
        if($? -eq $false) {
            throw
        } else {
            WriteOutput "Trying to pull the latest docker images" "DarkGray"
            docker pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:PHISHING_REPO 
            docker pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:PASSWORD_REPO
            #docker pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:DOWNLOAD_REPO
            WriteOutput "Succesfully pulled the docker images" "Green"
        }
    } catch {
        WriteOutput "Something went wrong while login into docker or pulling the repositories" "Red"
        Write-Warning $Error[0]
        WriteOutput "Resetting all changes" "Red"
        Remove-Item -Path $rootPath -Recurse
        Set-Content -Path $hostFile -Value (get-content -Path $hostFile | Select-String -Pattern '#MPSE' -NotMatch)
        Remove-MpPreference -ExclusionPath $rootPath
        Exit 1
    }

    # Create Shortcut and autostart entry
    try {
        WriteOutput "Try to create a new autostart entry" "DarkGray"
        $WshShell = New-Object -comObject WScript.Shell -ErrorAction Stop
        $Shortcut = $WshShell.CreateShortcut($shortcutPath)
        $Shortcut.TargetPath = "$directoryPath\app.exe"
        $Shortcut.WindowStyle = 7
        $Shortcut.Save()
        WriteOutput "Created an autostart entry" "Green"  
    }
    catch {
        WriteOutput "Something went wrong creating the autostart entry" "Red"
        Write-Warning $Error[0]
        WriteOutput "Resetting all changes" "Red"
        Remove-Item -Path $rootPath -Recurse
        Set-Content -Path $hostFile -Value (get-content -Path $hostFile | Select-String -Pattern '#MPSE' -NotMatch)
        Remove-MpPreference -ExclusionPath $rootPath
        Exit 1
    }
                  
} Else {
    WriteOutput "The given folder path $directoryPath already exists" "DarkGray"
    try {
        $Answer = Read-Host -Prompt "Do you really want to uninstall the native app? `n Type (y)es or (n)o" -ErrorAction Stop
        if ($Answer -eq "y" -or $Answer -eq "yes") {
            WriteOutput "Trying to uninstall" "DarkGray"

            # Kill process if exists
            WriteOutput "Trying to kill the nativeapp process" "DarkGray"
            Get-Process | Where-Object { $_.Name -eq "app" } | Select-Object -First 1 | Stop-Process -ErrorAction Stop
            WriteOutput "Killed the process if exists" "Green"

            # Remove folder
            WriteOutput "Trying to remove the folder: $rootPath" "DarkGray"
            Remove-Item -Path $rootPath -Recurse -Force -ErrorAction Stop
            WriteOutput "Removed the folder with all files: $rootPath" "Green"
            
            # Remove Windows Defender Exception
            WriteOutput "Trying to remove the exclusion from Windows Defender" "DarkGray"
            Remove-MpPreference -ExclusionPath $rootPath -ErrorAction Stop
            WriteOutput "Removed the exclusion from Windows Defender" "Green" 

            # Remove autostart
            WriteOutput "Trying to remove the autostart entry" "DarkGray"
            Remove-Item -Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\nativeapp.lnk" -ErrorAction Stop
            WriteOutput "Removed the autostart entry" "Green"

            # Remove Host entry
            WriteOutput "Removing host entry" "DarkGray"
            Set-Content -Path $hostFile -Value (get-content -Path $hostFile | Select-String -Pattern '#MPSE' -NotMatch) -ErrorAction Stop
            WriteOutput "Removed successfully host entry" "Green"
        }
    }
    catch {
        WriteOutput "Something went wrong creating the autostart entry" "Red"
        Write-Warning $Error[0]
        Exit 1
    }
}
