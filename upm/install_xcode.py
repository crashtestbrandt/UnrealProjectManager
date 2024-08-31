import os
import sys
import subprocess

XCODE_VERSION = "14.1"

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def run_as_admin():
    if not is_admin():
        print("This script requires administrator privileges. Please run it with 'sudo'.")
        sys.exit(1)

def install_homebrew():
    print("Checking if Homebrew is installed...")
    try:
        subprocess.run(["brew", "--version"], check=True)
        print("Homebrew is already installed.")
    except subprocess.CalledProcessError:
        print("Homebrew not found. Installing Homebrew...")
        try:
            subprocess.run(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                shell=True,
                check=True
            )
            print("Homebrew installation complete.")
        except subprocess.CalledProcessError as e:
            print(f"Homebrew installation failed: {e}")
            sys.exit(1)

def install_xcodes():
    print("Checking if 'xcodes' is installed...")
    try:
        subprocess.run(["xcodes", "--version"], check=True)
        print("'xcodes' is already installed.")
    except subprocess.CalledProcessError:
        print("'xcodes' not found. Installing 'xcodes' via Homebrew...")
        try:
            subprocess.run("brew install robotsandpencils/made/xcodes", shell=True, check=True)
            print("'xcodes' installation complete.")
        except subprocess.CalledProcessError as e:
            print(f"'xcodes' installation failed: {e}")
            sys.exit(1)

def install_xcode_version(version):
    print(f"Installing Xcode {version} using 'xcodes'...")
    try:
        subprocess.run(f"xcodes install {version}", shell=True, check=True)
        print(f"Xcode {version} installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Xcode {version} installation failed: {e}")
        sys.exit(1)

def agree_to_license():
    print("Agreeing to Xcode license...")
    try:
        subprocess.run("sudo xcodebuild -license accept", shell=True, check=True)
        print("Xcode license agreed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to agree to Xcode license: {e}")
        sys.exit(1)

def setup_xcode_for_unreal():
    print("Configuring Xcode for Unreal Engine development...")
    try:
        subprocess.run("sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer", shell=True, check=True)
        subprocess.run("sudo xcodebuild -runFirstLaunch", shell=True, check=True)
        print("Xcode is now configured for Unreal Engine development.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to configure Xcode: {e}")
        sys.exit(1)

def setup_environment():
    run_as_admin()
    
    install_homebrew()
    install_xcodes()
    install_xcode_version(XCODE_VERSION)
    agree_to_license()
    setup_xcode_for_unreal()

if __name__ == "__main__":
    setup_environment()
