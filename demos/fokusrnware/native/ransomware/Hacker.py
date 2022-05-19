import sys
from subprocess import PIPE, DEVNULL, STDOUT, call, Popen
from ctypes import windll
from playsound import playsound
from re import findall
from time import sleep
from tkinter import Button, Label, Tk
from PIL import Image, ImageTk
import winsound


'''
    The user is accompanied through a cyberattack of the demonstator and is informed about the individual events and actions of the Maleware-Attack
    with the help of the "HackerBox". The Hacker-Class can also kill processes and add the himself as a trusted software, which bypasses Windows-Defender Ransomware-Potection.
    In addition, there are other functionalities that contribute to the experience of the 
    scenario, such as the opening of several command prompts with ascii art and the playing of sound effects. 
     
'''

class Hacker:

    CREATE_NO_WINDOW = 0x08000000 # Flag for not opening new console, when executing a shell command

    def __init__(self, asciiArt="", messages=dict(), soundeffects=dict(), messageIcon="", messageBackground="", user="") -> None:
        self.asciiArt = asciiArt
        self.messages = messages
        self.soundeffects = soundeffects
        self.messageIcon = messageIcon
        self.messageBackground = messageBackground
        self.user = user


    '''
        checks if this programm is executed with admin privileges
        @return: bool value, wheter admin rights are available or not
    '''
    def checkAdminRights(self) -> bool:
        return windll.shell32.IsUserAnAdmin() != 0

    
    '''
        Opens a command prompt, where the rights of the user are showed. After 5 Seconds the terminal will be closed
    '''
    def showUserAdminRights(self) -> None:
        #if self.checkAdminRights() == False:
        #    return
        timeout = 6 
        call('start cmd /k \"net user ' + self.user + '\"', shell = True)
        sleep(timeout) # so the timeout in that spawned command prompt can be readed
        tasklistResult = Popen("tasklist", stdout=PIPE, stderr=STDOUT, stdin=DEVNULL) # saving the result of tasklist command 
        tasklistResult = tasklistResult.stdout.read()
        reg = findall(r"cmd.exe\s+([0-9]+) Console", tasklistResult.decode("utf-8")) # filter the pids from the result through regex
        call('taskkill /pid ' + reg[-1] + ' /f')
    
        

    '''
        Tries to kill a process by name with a taskkill command
        @param name: name of the process
    '''
    def kProcessByName(self, processName) -> None:
        call('taskkill /f /t /im ' + processName, shell = True, creationflags=self.CREATE_NO_WINDOW) #That line is for the drive-by-download attackvector

    
    '''
        Plays a soundfile
        @param soundKey: sound key, for identifing which sound will be played
    '''   
    def playSound(self, soundKey) -> None:
        if soundKey == "":
            return
        #print(self.soundeffects[soundKey])
        #playsound(u''.format(self.soundeffects[soundKey]))
        winsound.PlaySound(self.soundeffects[soundKey], winsound.SND_FILENAME)

    '''
        Pops up a text box on the Screen with icon and background image.
        In addition, the user can interact with the textbox by clicking on "ok".
        @param messageKey: message key, for identifing which message will be displayed
    '''
    def hackerBox(self, messageKey) -> None:
        if self.messages[messageKey] == "" or self.messageIcon == "" or self.messageBackground == "":
            return
        message = str(self.messages[messageKey])
        messages = message.split("\+")
        for msge in messages:
            root = Tk() 
            root.title("HackerBox")
            root.iconbitmap(self.messageIcon)
            b = Image.open(self.messageBackground, mode='r')
            pic = ImageTk.PhotoImage(b)
            boxPic = Label(root, image=pic, bg="blue")
            boxPic.place(x=0, y=0, relwidth=1, relheight=1)
            boxText = Label(root, text=msge) 
            boxText.pack(pady=50, padx=50) 
            boxText.configure(font=("Times New Roman", 12, "bold"),background="black", foreground="lightgreen")
            okButton = Button(root, text="ok", command=root.destroy)
            okButton.pack(pady=70)
            root.wm_attributes('-transparentcolor', 'blue')
            root.lift()
            root.update()
            root.mainloop() 

    
    '''
        Opens a lot of consoles with a skull-ascii-art, which are then stopped again 
        with the help of their a pid with a reversed order.
        This method serves to increase the attention of the demonstrator-user.
    '''
    def consoleBomb(self) -> None:
        if self.asciiArt == "":
            return
        for i in range(20):
            p = Popen(["start", "cmd", "/k", "color 0a &  type " + self.asciiArt], shell = True)
            sleep(0.05) # with this, it will look more sequetially, when the cmds get opened
        sleep(2) # waiting 2 seconds, so the ascii-art can load inside the cmds before closing them again
        tasklistResult = Popen("tasklist", stdout=PIPE, stderr=STDOUT, stdin=DEVNULL) # saving the result of tasklist command 
        tasklistResult = tasklistResult.stdout.read()
        reg = findall(r"cmd.exe\s+([0-9]+) Console", tasklistResult.decode("utf-8")) # filter the pids from the result through regex
        '''if len(reg) > 20:
            reg.pop(0) # dev console pid
        for i in reversed(range(len(reg))): 
            call("Taskkill /PID "+ reg[i] + " /F", shell = True, creationflags=self.CREATE_NO_WINDOW)
            sleep(0.05)'''
        for i in range(20):
            idx = len(reg) - 1 - i
            call("Taskkill /PID "+ reg[idx] + " /F", shell = True, creationflags=self.CREATE_NO_WINDOW)
            sleep(0.05)
    
    def mailWormShow(self):
        usernameList= ['Nina.Folan@mpseinternational.com', 'Maurius.Schneider@mpseinternational.com', 'Zac.Efron@mpseinternational.com', 'Angelina.Cuphoald@mpseinternational.com', 'Chistiane.Ziesing@mpseinternational.com']
        for username in usernameList:
            Popen("\"C:\\Program Files\\Mozilla Thunderbird\\thunderbird\" -compose \"to='" + username + "',subject='Sensible Daten auf deinem LinkedIn Profil',body='Hallo, <br><br>Auf deinem Profil in LinkedIn sind sensible persönliche und unser Unternehmen betreffende Informationen eingetragen worden. Schau dir das bitte mal auf LinkedIn an <a href=""https://de.linkedln.com/myprofile"">https://de.linkedln.com/myprofile</a> <br><br>Viele Grüße'\"", shell = True, creationflags=self.CREATE_NO_WINDOW, stdout=None, stderr=None, stdin=None, close_fds=True)
            sleep(0.5)
        sleep(3)
        call("taskkill /f /im thunderbird.exe", shell = True, creationflags=self.CREATE_NO_WINDOW)
        
    

