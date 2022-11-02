import subprocess
import sys


def sync_wsl():
    """
    Syncs the WSL hwclock and systemclock to the windows time to work around
    several Windows related bugs.
    """
    if sys.platform == "win32":
        cmd = ["powershell", "Get-Date", "-Format", "\"yyyy-MM-dd HH:mm:ss\""]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, _ = p.communicate()
        cmd = ["wsl", "--user", "root", "hwclock", "--set", "--date", out]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.communicate()
        cmd = ["wsl", "--user", "root", "hwclock", "-s"]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.communicate()
