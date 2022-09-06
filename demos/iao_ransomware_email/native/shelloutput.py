import os
import time


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


def shelloutput():
    print('##########################################')
    print('###########     Ransomware     ###########')
    print('##########################################')

    print('Generating encryption key...')
    time.sleep(.5)
    print('Done.\n')

    time.sleep(.125)
    print('Locating user homepath...')
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    dirName = desktop
    time.sleep(.25)
    print('Done.\n')

    time.sleep(.125)
    print('Locating files to encrypt...')
    files = getListOfFiles(dirName)
    print('Done.\n')

    print('Encrypting files...')

    for filename in files:
        print('Encrypting ', filename)
        time.sleep(.075)
    print('Done.\n')

    print('Change wallpaper...')
    print('Done.')
    time.sleep(5)

    return


if __name__ == "__main__":
    shelloutput()
