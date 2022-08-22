All setup steps in this guide need to be done on a Windows workstation to have a compatible client for the ELITE platform. 

The client specification is as follows:
- Windows as OS (most common and insecure OS in our target audience)
- All prerequisites stated in *Initial OS setup* are installed
- The *NativeApp* component is installed and running
- Each demo can require further software (like an e-mail client) which must then be installed natively on the host machine. These should be covered in the *Initial OS setup* steps below.

### Initial OS setup
After the installation of a fresh Windows 10 instance we need to install some basic tools and configure the OS to allow us to use the platform.
You can either install and setup everything manually or use powershell commands for (almost) everything.

You need to run following command in the powershell. It is split into multiple stages per reboot.

**Stage 1: Update Windows**

Run PowerShell as administrator

```powershell
# PowerShell as administrator
Set-ExecutionPolicy Bypass -scope Process -Force
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
Install-Module PSWindowsUpdate -Force
Get-WindowsUpdate -AcceptAll -Install -AutoReboot
```

**Stage 2: Install WSL2**

Run PowerShell as user

```powershell
# Install wsl2 (as user - not admin!)
# source: https://webinstall.dev/wsl2/
curl.exe -A "MS" https://webinstall.dev/wsl2 | powershell
Restart-Computer
```

**Stage 3: Setup WSL2**

You have to *manually* [install the linux kernel update package for WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package) before running the commands below.

Run PowerShell as user

```powershell
wsl --set-default-version 2
wsl --install -d Ubuntu-20.04
Restart-Computer
```

**Stage 4: Install dependencies**

Run PowerShell as administrator

```powershell
# Install chocolatey package manager
Set-ExecutionPolicy Bypass -scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
# install dependencies via chocolatey
choco install python firefox thunderbird git nssm -y

wsl --user root apt update
wsl --user root apt install docker.io

wsl --user root mkdir -p /root/.docker/cli-plugins
wsl --user root bash -c "curl -SL https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64 -o /root/.docker/cli-plugins/docker-compose && chmod +x /root/.docker/cli-plugins/docker-compose"


Restart-Computer
```


### Installation of Native Access Component
The full installation process can be found under the [Native App page](https://code.fbi.h-da.de/groups/esc-mpse20/-/wikis/Demonstrations/Native-App#install)

Further the `rootCA.crt` has to be imported into the browser of your choice (accept identification of websites), it can be found in the program directory of the nativeapp (created through the installation) `C:\Program Files(x86)\hda\nativeapp\stacks`.

**Troubleshooting**
- There have been issues with 3rd party antivirus programs - Windows Defender not affected (see [Native App - Issues](Demonstrations/Native-App#issues)), it's recommended to use defender.
- Problem: "Error: "This installation package could not be opened. Contact the application vendor to verify that this is a valid Windows Installer package."
- Solution: If opened within the WSL environment you need to copy it into the local filesystem and run it from there.

### Execution of Native Access Component

Will be launched on every login of the user automatically. If you wan't to start it manually you have to go to the installation folder `C:\Program Files(x86)\hda\nativeapp` and run `./venv/Scripts/nativeapp -p .`. This client handles start/stop of docker containers for demos and provides functionalities that can't be covered through docker containers alone.


### Pulling the latest docker images
The native app installer is pulling automatically the newest images. If an error appears you have to download manually.

To locally build the containers run the `build_images.sh` script in a Linux environment (this includes WSL).
