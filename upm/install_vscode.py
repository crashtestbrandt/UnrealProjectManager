import os
import sys
import subprocess
import urllib.request

VSCODE_INSTALLER_URL = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"

def download_vscode_installer(download_path):
    # URL for the Visual Studio Code installer (system installer for 64-bit Windows)
    installer_url = VSCODE_INSTALLER_URL
    
    # Path to save the installer
    installer_path = os.path.join(download_path, "VSCodeUserSetup-x64.exe")
    
    print(f"Downloading Visual Studio Code installer to {installer_path}...")
    try:
        urllib.request.urlretrieve(installer_url, installer_path)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download Visual Studio Code installer: {e}")
        sys.exit(1)
    
    return installer_path

def install_vscode():
    download_path = r"C:\Temp"
    os.makedirs(download_path, exist_ok=True)
    vscode_installer_path = download_vscode_installer(download_path)
    print(f"Visual Studio Code installer downloaded to: {vscode_installer_path}")

    # Command to silently install VS Code
    #command = f'"{vscode_installer_path}" /silent /mergetasks=!runcode'
    command = f'"{vscode_installer_path}" /mergetasks=!runcode'

    try:
        print("Starting Visual Studio Code installation...")
        subprocess.run(command, shell=True, check=True)
        print("Installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_vscode()
