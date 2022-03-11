#Python3 version of hugo24's snippet
import winreg
import pyuac
import os

debug = False

#Get Path
path = os.path.dirname(os.path.realpath(__file__))

if " " in path:
    print("ERROR! File is inside a folder that contains spaces, try replacing it with - or _.")
else:
    if pyuac.isUserAdmin() == True or debug == True:
        REG_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

        def set_reg(name, value):
            try:
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH)
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, 
                                            winreg.KEY_WRITE)
                winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
                winreg.CloseKey(registry_key)
                return True
            except Exception as e:
                print(e)
                return False

        def get_reg(name):
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0,
                                            winreg.KEY_READ)
                value, regtype = winreg.QueryValueEx(registry_key, name)
                winreg.CloseKey(registry_key)
                return value
            except WindowsError:
                return None

        #Example MouseSensitivity
        #Read value 
        #print (get_reg('rpc'))

        #Set Value 1/20 (will just write the value to reg, the changed mouse val requires a win re-log to apply*)
        #print(set_reg('autostarttest', str("hilfeIchbinhiergefangen")))
        
        
        #Ask for Program Name (case sensitive)
        script = input("Welcome to your Script-Autostart generator!\nBe careful to run this script in the directory that your Script is in\nScript-Name(case sensitive + .py or .pyw) : ")
        
        scriptpath = str(path+"\\"+script)
        
        #Create Batch
        with open("startScript.bat", "w") as f:
            f.write(f'@echo off\n\ncd "{path}"\npy "{script}"\n\n@pause')
        
        #Create vbs
        with open("autoStartBAT.vbs", "w") as f:
            f.write(f'CreateObject("Wscript.Shell").Run "{path}\startScript.bat", 0, True')
        
        #Write vbs to regestry
        set_reg(f'{script}', str(f'{path}\\autoStartBAT.vbs'))
        
        #Warn that changing the location will result in the autostart to not work anymore
        print("Done!\nPlease keep in mind that changing the file location will result in errors, delete the regestry key before doing so.")
        
        print(f"DEBUG:\n\n{get_reg(script)}")
        

    else:
        pyuac.runAsAdmin()