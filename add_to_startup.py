import os

def create_startup_script():
    cwd = os.getcwd()
    
    # Path to the Python script
    python_script_path = os.path.join(cwd, 'filter.py')
    
    # Content for the CMD file
    cmd_content = 'python "{}"\n'.format(python_script_path)
    
    # Path to the startup directory
    startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    
    # Path to the CMD file in the startup directory
    cmd_file_path = os.path.join(startup_dir, 'torrent_filter.cmd')
    
    # Write content to the CMD file
    with open(cmd_file_path, 'w') as cmd_file:
        cmd_file.write(cmd_content)
    
    print("Startup script created successfully!")

if __name__ == "__main__":
    create_startup_script()