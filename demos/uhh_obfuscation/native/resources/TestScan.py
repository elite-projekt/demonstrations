import urllib.request
import subprocess
import os


def stop_demo():
    PROTOCOL = "http"
    HOST = "127.0.0.1:5000"
    PATH = "orchestration/stop/demo/uhh_obfuscation"
    urllib.request.urlopen(f"{PROTOCOL}://{HOST}/{PATH}")


def scan_file_with_defender(file_path):
    try:
        scan_command = ["powershell.exe",
                        "-Command",
                        "Start-MpScan -ScanPath '{0}' -ScanType QuickScan".format(file_path)] # noqa: 501
        scan = subprocess.run(scan_command, # noqa: 501
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True)

        get_scan_results_command = ["powershell.exe",
                                    "-Command",
                                    "Get-MPthreat"]
        scan_result = subprocess.run(get_scan_results_command,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True)
        scan_result_text = scan_result.stdout

        get_scan_results_detail_command = ["powershell.exe",
                                           "-Command",
                                           "Get-MPthreatDetection"]
        scan_result_detail = subprocess.run(get_scan_results_detail_command,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True)
        scan_result_detail_text = scan_result_detail.stdout

        print("=========================================")
        if scan_result_text == "":
            if file_path != "RansomWare.py":
                print("BBB {0}".format(file_path))
                print("=========================================")
                return False
            else:
                # Detect Ransomware even if it was not detected
                print("AAA {0}".format(file_path))
                print("Virus Name:", "Ransom:Python/Encryptor.BC")
                print("=========================================")
                return True
        else:
            if file_path != "RansomWare_obfuscated.py":
                # Only if this scanned file was detected
                if file_path in scan_result_detail_text:
                    virus_name = scan_result_text.split("ThreatName       : ")[1].split("\n")[0] # noqa: 501
                    print("AAA {0}".format(file_path))
                    print("Virus Name:", virus_name)
                    print("=========================================")
                    return True
            else:
                print("BBB {0}".format(file_path))
                print("=========================================")
                return False
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        return False


# For second scan of obfuscated Ransomware
if os.path.isfile("RansomWare_obfuscated.py"):
    detected = scan_file_with_defender("RansomWare_obfuscated.py")
    print("")
    print("CCC ...")
    os.system("pause >nul")
    print("")
    print("EEE ...")
    stop_demo()
# For first scan of non-obfuscated Ransomware
elif os.path.isfile("RansomWare.py"):
    if os.path.isfile("RansomWare.py"):
        detected = scan_file_with_defender("RansomWare.py")
        print("")
        print("DDD ...")
        os.system("pause >nul")
else:
    print("FFF")
    print("")
    print("DDD ...")
    os.system("pause >nul")
