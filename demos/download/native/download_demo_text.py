class DownloadDemoText:
    script = "" + \
        "\n@echo off\n" + \
        "chcp 1252>nul\n" + \
        "set ue=ü\n" + \
        "set ae=ä\n" + \
        "set oe=ö\n" + \
        "set Uue=Ü\n" + \
        "set Aae=Ä\n" + \
        "set Ooe=Ö\n" + \
        "set ss=ß\n" + \
        "chcp 850>nul\n" + \
        "echo ########################################################" + \
        "####\n" + \
        "echo: \n" + \
        "echo     W%ae%re dies keine Demo, w%ae%ren Sie nun " + \
        "gehackt worden\necho: \n" + \
        "echo #########################################################" + \
        "###\n" + \
        "echo: \n" + \
        "echo Sie waren ungesch%ue%tzt auf einer infizierten Website und " + \
        "sind\n" + \
        "echo Opfer eines Drive-By Downloads geworden. Ein Drive-By " + \
        "Download\n" + \
        "echo ist ein Download, der ohne Ihr Wissen durchgef%ue%hrt " + \
        "werden kann.\n" + \
        "echo: \n" + \
        "echo Dem Angreifer in diesem %Uue%bungsszenario ist es " + \
        "gelungen, eine \necho Datei " + \
        "mit Schadsoftware auf Ihren Desktop " + \
        "herunterzuladen und \necho auszuf%ue%hren. " + \
        "Im Zuge dieses Angriffs wurde auf ihrem Desktop \necho zudem " + \
        "eine Textdatei namens \"download-demo.txt\" erzeugt. Suchen \n" + \
        "echo und %oe%ffnen Sie diese Datei jetzt. " + \
        "Sie enth%ae%lt Informationen \necho zum weiteren " + \
        "Verlauf der Demo. \necho: \n" + \
        "echo Sobald Sie die Datei \"download-demo.txt\" ge%oe%ffnet " + \
        "haben, k%oe%nnen \necho Sie dieses Fenster " + \
        "durch dr%ue%cken einer beliebigen Taste schlie%ss%en.\n" + \
        "echo: \n" + \
        "pause\n" + \
        "exit"
