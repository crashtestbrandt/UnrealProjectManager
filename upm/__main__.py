import argparse
import sys
import os
import subprocess

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def run_as_admin(cmd):
    if sys.version_info >= (3, 5):
        cmd = cmd
        subprocess.run(cmd, shell=True)
    else:
        raise RuntimeError("Python 3.5+ is required to run this script.")

def valid_file_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"Invalid file path: {path}")

def valid_dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"Invalid directory path: {path}")

def create_directory(path):
    # Use os.makedirs to create the directory if it doesn't exist
    try:
        os.makedirs(path, exist_ok=True)  # exist_ok=True prevents an error if the directory already exists
        return os.path.abspath(path)
    except OSError as e:
        raise argparse.ArgumentTypeError(f"Error creating directory {path}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Unreal Project Manager CLI",
        prog="upm"
    )

    subparsers = parser.add_subparsers(dest='command')

    parser_setup = subparsers.add_parser('config', help='Copy upm configuration files to a destination folder.')
    parser_setup.add_argument('--dir', type=create_directory, help='Destination folder (current directory if not specified).', default='.')
    parser_setup.add_argument('--gitignore', action='store_true', help='Add UPM .gitignore file to destination folder.')
    parser_setup.add_argument('--unreal', type=valid_dir_path, help='Specify Unreal Engine path. If not specified, the default install path for your platform will be used.')
    parser_setup.add_argument('--project_name', type=str, help='Specify the name for your project. If not specified, the name of the current directory will be used.')
    parser_setup.add_argument('--workspace', type=str, help='Specify the name for your VS Code workspace. If not specified, the name of the current directory will be used.')
    parser_setup.add_argument('--changelog', type=str, help='Specify changelog filename.', default='Changelog.json')
    
    parser_setup.add_argument('--clean', action='store_true', help='Clean generated project files.')

    parser_setup = subparsers.add_parser('setup', help='Run setup script.')
    parser_setup.add_argument('--clean', action='store_true', help='Clean generated project files.')

    parser_setup = subparsers.add_parser('install-vscode', help='Download and install Visual Studio Code.')
    parser_setup = subparsers.add_parser('install-vs', help='Download and install Visual Studio Community (prompts for admin privileges).')
    parser_setup = subparsers.add_parser('install-xcode', help='Download and install XCode.')

    parser_setup = subparsers.add_parser('build', help='Build commands.')
    parser_setup.add_argument('--project-dir', type=str, required=True,
                        help="Path to the Moonshot project directory")
    parser_setup.add_argument('--build-type', type=str, required=True,
                        help="Type of build (debug, development, testomg. release)")
    parser_setup.add_argument('--target-name', type=str, required=True,
                        help="Type of build (debug, development, testomg. release)")
    parser_setup.add_argument('--clean', action='store_true',
                        help="Clean selected targets")
    parser_setup.add_argument('--build', action='store_true',
                        help="Build selected targets")
    parser_setup.add_argument('--package', action='store_true',
                        help="Package selected target for deployment")

    args = parser.parse_args()

    if args.command == 'config':
        from upm.config import config
        config(args)
    elif args.command == 'setup':
        from upm.setup import setup
        setup(args)

    elif args.command == 'install-vscode':
        from upm.install_vscode import install_vscode
        install_vscode()

    elif args.command == 'install-vs':
        if not is_admin():
            print("Re-running script with elevated privileges...")
            cmd = [
                'powershell', 
                'Start-Process', sys.executable, 
                '-ArgumentList', '"-m upm install-vs"', 
                '-Verb', 'runAs'
            ]
            run_as_admin(cmd)
        else:
            from upm.install_vs import install_visual_studio
            install_visual_studio()
    
    elif args.command == 'upmconfig':
        from upm.config import upmconfig
        upmconfig(args)
    
    elif args.command == 'build':
        from upm.build import build_project
        build_project(
            build_type=args.build_type,
            target_name=args.target_name,
            project_path=args.project_dir,
            clean=args.clean,
            build=args.build,
            package=args.package
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
