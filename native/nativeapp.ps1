#nativeapp.bat has to be started first

Write-Host "                                      ___                           ";
Write-Host " |\ |  _. _|_ o     _   /\  ._  ._     |  ._   _ _|_  _. | |  _  ._ ";
Write-Host " | \| (_|  |_ | \/ (/_ /--\ |_) |_)   _|_ | | _>  |_ (_| | | (/_ |  ";
Write-Host "                            |   |                                   ";

# Get working directory. Should be /demonstrations/native
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

# Check folder
$directoryPath="C:\Program Files (x86)\hda\nativeapp"
$rootPath="C:\Program Files (x86)\hda\"
$shortcutPath = "$Home\Desktop\nativeapp.lnk"
If(!(Test-Path -path $rootPath)) {
    $null = New-Item -Path $rootPath -ItemType directory
    Write-Host "====================================="
    Write-Host "Folder path has been created successfully at: " $rootPath
    Write-Host "====================================="

    # Check system language
    $lang = [CultureInfo]::InstalledUICulture
    if($lang -eq "de-DE") {
        $objUser = New-Object System.Security.Principal.NTAccount("VORDEFINIERT\Benutzer")
    } else {
        $objUser = New-Object System.Security.Principal.NTAccount("BUILTIN\USER")
    }
    # Setting directory security
    $colRights = [System.Security.AccessControl.FileSystemRights]"Modify" 
    $inheritanceFlag = [System.Security.AccessControl.InheritanceFlags]"ContainerInherit, ObjectInherit" 
    $propagationFlag = [System.Security.AccessControl.PropagationFlags]::None 
    $objType =[System.Security.AccessControl.AccessControlType]::Allow
    $objACE = New-Object System.Security.AccessControl.FileSystemAccessRule($objUser, $colRights, $inheritanceFlag, $propagationFlag, $objType)
    $objACL = Get-Acl -Path $rootPath
    $objACL.AddAccessRule($objACE)
    Set-ACL $rootPath $objACL
    Write-Host "====================================="
    Write-Host "Set directory security"
    Write-Host "====================================="

    $null = New-Item -ItemType Directory -Path $directoryPath
    Write-Host "====================================="
    Write-Host "Folder path has been created successfully at: " $directoryPath
    Write-Host "====================================="

    # Copy data
    if($isReleaseDirectory) {
        Copy-Item ".env" -Destination $directoryPath
        Copy-Item "stacks\" -Destination "$directoryPath\stacks" -Recurse -Force
        Copy-Item "rootCA.crt" -Destination "$directoryPath\stacks"
        Copy-Item "profiles" -Destination "$directoryPath" -Recurse
        Copy-Item "app.exe" -Destination "$directoryPath" 
    } else {
        Copy-Item "$workingDirectory\..\.env" -Destination $directoryPath
        Copy-Item "$workingDirectory\stacks\" -Destination "$directoryPath\stacks" -Recurse -Force
        Copy-Item "$workingDirectory\..\demoCA\rootCA.crt" -Destination "$directoryPath\stacks"
        Copy-Item "$workingDirectory\src\profiles" -Destination "$directoryPath" -Recurse
        Copy-Item "$workingDirectory\src\dist\windows\app.exe" -Destination "$directoryPath" 
    }

    Write-Host "====================================="
    Write-Host "Copied files to the created folder"
    Write-Host "====================================="
    
    # Host File
    $hostFile = "C:\Windows\System32\drivers\etc\hosts"
    $localRedirects = "127.0.0.1`twww.shipment-support-amazon.com covidsupportgermany.de coronahilfengermany.de mpseinternational.com mail.domain.com printer.io #MPSE"
    $containsRedirecets = Select-String -Path $hostFile -Pattern '#MPSE'
    try {
        if($containsRedirecets -ne $null) {
            Write-Host "====================================="
            Write-Host "Updating 127.0.0.1 entry"
            Write-Host "====================================="
            $line = Get-Content $hostFile | Select-String '#MPSE' | Select-Object -ExpandProperty Line
            $content = Get-Content $hostFile
            $content | ForEach-Object {$_ -replace $line, $localRedirects} | Set-Content $hostFile
        } else {
            Write-Host "====================================="
            Write-Host "Write redirects to end of hosts-file"
            Write-Host "====================================="
            Add-Content -Path $hostFile -Value "`n$localRedirects"
        }
    } catch {
        Write-Host -ForegroundColor Red "Can't write hostfile, add the following entries manually:`n $localRedirects"
    }

    # Set Windows Defender Exception
    Add-MpPreference -ExclusionPath $rootPath
    Write-Host "====================================="
    Write-Host "Added Exclusion in Windows Defender for native app"
    Write-Host "====================================="

    if($isReleaseDirectory) {
        Set-PsEnv
    } else {
        Set-PsEnv "$workingDirectory\..\.env"
    }

    # Information
    Write-Host "====================================="
    Write-Host -ForegroundColor Red "Information"
    Write-Host -ForegroundColor Green "To cover all dependencies please do the following:"
    Write-Host -ForegroundColor Green " - Have Docker for windows with the Linux subsystem installed"
    Write-Host -ForegroundColor Green " - Install the Thunderbird mail client on the system"
    Write-Host -ForegroundColor Green " - Import the 'rootCA.crt' certificate (provided via the program folder) into the browser of your choice - [trust identifying websites]"
    Write-Host -ForegroundColor Green " - pull the latest images for the demos`n"
    Write-Host -ForegroundColor Green "Docker images for the demos:"
    Write-Host "docker login $Env:REGISTRY_URL"
    Write-Host "docker pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:PHISHING_REPO"
    Write-Host "docker pull $Env:REGISTRY_URL/$Env:GROUP_NAME/demonstrations/$Env:PASSWORD_REPO"
    Write-Host "====================================="

    # Create Shortcut
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = "$directoryPath\app.exe"
    $Shortcut.WindowStyle = 7
    $Shortcut.Save()
    Write-Host "====================================="
    Write-Host "Created a shortcut on the desktop"
    Write-Host "====================================="

    # Create autostart entry
    Copy-Item $shortcutPath -Destination "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
    Write-Host "====================================="
    Write-Host "Created an autostart entry"
    Write-Host "====================================="

               
} Else {
    # Remove folder
    Write-Host "====================================="
    Write-Host "The given folder path $directoryPath already exists"
    Write-Host "====================================="
    Write-Host "====================================="
    Write-Host "Trying to deinstall"
    Write-Host "====================================="
    Remove-Item -Path $rootPath -Recurse
    Write-Host "====================================="
    Write-Host "Removed the folder with all files: " $rootPath
    Write-Host "====================================="
    
    # Remove Windows Defender Exception
    Remove-MpPreference -ExclusionPath $rootPath
    Write-Host "====================================="
    Write-Host "Removed the exclusion from Windows Defender"
    Write-Host "====================================="

    # Remove shortcut on desktop
    Remove-Item -Path $shortcutPath
    Write-Host "====================================="
    Write-Host "Removed shortcut on desktop"
    Write-Host "====================================="

    # Remove autostart
    Remove-Item -Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\nativeapp.lnk"
    Write-Host "====================================="
    Write-Host "Removed the autostart entry"
    Write-Host "====================================="
}
