import os


class download_demo:
    def create_fake_malware():
        print("creating fake malware...")

        path = os.path.join(
            os.path.join(os.environ['USERPROFILE']), 'Desktop')
        filename = os.path.join(path, "malware.bat")

        file = open(filename, "w")
        f = "@echo off\n"
        f += "echo ########################################################"
        f += "####\n"
        f += "echo: \n"
        f += "echo     Waere dies keine Demo, waeren Sie nun gehackt worden\n"
        f += "echo: \n"
        f += "echo #########################################################"
        f += "###\n"
        f += "echo: \n"
        f += "echo Sie waren ungeschuetzt auf einer infizierten Website und"
        f += "sind\n"
        f += "echo Opfer eines Drive-By Downloads geworden. Ein Drive-By"
        f += "Download\n"
        f += "echo ist ein Download, der ohne Ihr Wissen durchgefuehrt werden"
        f += "kann.\n"
        f += "echo: \n"
        f += "echo Im Folgenden wird Ihnen erklaert, wie Sie sich vor"
        f += "solchen\n"
        f += "echo Angriffen schuetzen koennen. Schliessen Sie dieses Fenster"
        f += "und\n"
        f += "echo kehren Sie zu ihrem Browser zurueck.\n"
        f += "echo: "
        f += "pause\n"
        f += "exit"

        file.write(f)
        file.close()

        os.system("start /wait cmd.exe @cmd /k \"" + filename + "\"")
