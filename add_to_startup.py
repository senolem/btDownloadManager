import os
from win32com.client import Dispatch

def create_startup_shortcut():
    # Get the current working directory
    cwd = os.getcwd()
    
    # Path to the Python script
    python_script_path = os.path.join(cwd, 'filter.pyw')
    
    # Path to the startup directory
    startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    
    # Path to save the shortcut
    shortcut_path = os.path.join(startup_dir, 'torrent_filter.lnk')
    
    # Create a shortcut to the Python script in the Startup directory
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = python_script_path
    shortcut.save()
    
    print("Startup shortcut created successfully!")

if __name__ == "__main__":
    create_startup_shortcut()
