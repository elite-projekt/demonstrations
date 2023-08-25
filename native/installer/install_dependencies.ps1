[CmdletBinding()]
param (
    [Parameter()]
    [switch]
    $Boot
)

if ($Boot) {
	Write-Output "Installing WSL. Since the servers from Microsoft tend to be very slow, this can take a while..."
    # Just in Case: do it again
    choco install wsl2 --params "/Version:2" -y
    wsl --set-default-version 2
    #curl.exe -L -o $env:TEMP/ubuntu.appx http://192.168.122.1:8000/wslubuntu2004
    curl.exe -L -o $env:TEMP/ubuntu.appx https://aka.ms/wslubuntu2204
    Add-AppxPackage $env:TEMP/ubuntu.appx
    rm $env:TEMP/ubuntu.appx

    $username = "elite"
    $password = "elite"

    ubuntu.exe install --root

    # create user account
    wsl -u root useradd -m "$username"
    wsl -u root sh -c "echo `"${username}:${password}`" | chpasswd" # wrapped in sh -c to get the pipe to work
    wsl -u root  chsh -s /bin/bash "$username"
    wsl -u root usermod -aG adm,cdrom,sudo,dip,plugdev "$username"

    ubuntu.exe config --default-user "$username"


    # apt install -y isn't enough to be truly noninteractive
    $env:DEBIAN_FRONTEND = "noninteractive"
    $env:WSLENV += ":DEBIAN_FRONTEND"

    # update software
    wsl -u root apt-get update
    wsl -u root apt-get full-upgrade -y
    wsl -u root apt-get autoremove -y
    wsl -u root apt-get autoclean


    # Choco command commented, since doing it manually prevents a possible race condition since we still need to download the file
    #choco install wsl-ubuntu-2204 --params "/AutomaticInstall:true"

    # Fix WSL bug: https://github.com/microsoft/WSL/issues/6044
    wsl -u root update-alternatives --set iptables /usr/sbin/iptables-legacy
    wsl -u root update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy


    wsl --user root bash -c "apt update && apt install -y docker.io && mkdir -p /root/.docker/cli-plugins && curl -SL https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64 -o /root/.docker/cli-plugins/docker-compose && chmod +x /root/.docker/cli-plugins/docker-compose"
    # Do my thing after rebooting
    Get-ScheduledTask -TaskName "ContinueAfterBoot" | Unregister-ScheduledTask -Confirm:$false

}
else {
    # Do my thing before rebooting:
    Set-ExecutionPolicy Bypass -scope Process -Force
    Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
    Install-Module PSWindowsUpdate -Force
    Get-WindowsUpdate -AcceptAll -Install -IgnoreReboot
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    choco install python firefox thunderbird -y
    choco install wsl2 --params "/Version:2" -y

    # Setup task for after reboot:
    $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$PSCommandPath`" -Boot"
    $Trigger = New-ScheduledTaskTrigger -AtLogon
    $Principal = New-ScheduledTaskPrincipal -UserId $(whoami) -RunLevel Highest
    $Settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -RunOnlyIfNetworkAvailable
    Register-ScheduledTask -TaskName "ContinueAfterBoot" -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Description "Script After Boot Action"
    Restart-Computer
}
