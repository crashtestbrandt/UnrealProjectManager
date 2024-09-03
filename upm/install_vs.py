import os
import sys
import subprocess
import urllib.request

VS_INSTALLER_URL = "https://aka.ms/vs/17/release/vs_community.exe"

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def run_as_admin():
    if sys.version_info >= (3, 5):
        # Check if the script is run as a module
        module_flag = "-m" if hasattr(sys, 'frozen') else ""
        # Command to re-run the script with elevated privileges
        cmd = [
            'powershell', 
            'Start-Process', sys.executable, 
            '-ArgumentList', f'"{module_flag} {__name__} {" ".join(sys.argv[1:])}"', 
            '-Verb', 'runAs'
        ]
        subprocess.run(cmd, shell=True)
    else:
        raise RuntimeError("Python 3.5+ is required to run this script.")

def download_vs_installer(download_path):
    installer_url = VS_INSTALLER_URL
    installer_path = os.path.join(download_path, "vs_installer.exe")
    print(f"Downloading Visual Studio installer to {installer_path}...")
    try:
        urllib.request.urlretrieve(installer_url, installer_path)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download Visual Studio installer: {e}")
        sys.exit(1)
    return installer_path

def install_visual_studio():
    if not is_admin():
        print("Re-running script with elevated privileges...")
        run_as_admin()
        sys.exit(0)
    
    download_path = r"C:\Temp"
    os.makedirs(download_path, exist_ok=True)
    vs_installer_path = download_vs_installer(download_path)
    print(f"Visual Studio installer downloaded to: {vs_installer_path}")

    workloads = [
        "Microsoft.VisualStudio.Workload.ManagedDesktop",
        "Microsoft.VisualStudio.Workload.NativeDesktop",
        "Microsoft.VisualStudio.Workload.Universal",
        "Microsoft.VisualStudio.Workload.NativeGame"
    ]

    components = [
        "Microsoft.VisualStudio.Component.VC.DiagnosticTools",
        "Microsoft.VisualStudio.Component.Windows10SDK.18362"
    ]

    workload_args = " ".join([f"--add {workload}" for workload in workloads])
    component_args = " ".join([f"--add {component}" for component in components])

    command = (
        f'"{vs_installer_path}" --wait '
        f'--addProductLang en-US '
        f'{workload_args} '
        f'{component_args} '
        f'--includeRecommended --includeOptional --noStartAfterInstall'
    )

    try:
        print("Starting Visual Studio installation. Grab some coffee, this could take a while ...")
        subprocess.run(command, shell=True, check=True)
        print("Installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_visual_studio()