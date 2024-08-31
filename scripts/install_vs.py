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
        # Ensure that the script is run with elevated privileges
        subprocess.run(['powershell', 'Start-Process', sys.executable, '-ArgumentList', '"{}"'.format(' '.join(sys.argv)), '-Verb', 'runAs'], shell=True)
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
        f'"{vs_installer_path}" --quiet --wait '
        f'--addProductLang en-US '
        f'{workload_args} '
        f'{component_args} '
        f'--includeRecommended --includeOptional'
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
