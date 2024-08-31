import os
import platform
import subprocess
import argparse
from dotenv import load_dotenv

DOTENV_PATH = '.env'
UNREAL_PATH_KEY = 'UNREAL_PATH'
ARCHIVE_DIRECTORY = 'Packages'
DEFAULT_BUILD_TYPE = 'Development'

load_dotenv(DOTENV_PATH)

system = platform.system()

def build_project(project_dir, target_name, build_type=DEFAULT_BUILD_TYPE, build=False, clean=False, package=False):
    UNREAL_PATH = os.getenv(UNREAL_PATH_KEY)
    
    if UNREAL_PATH is None:
        raise Exception(f"Environment variable {UNREAL_PATH} not set")

    project_path = os.path.join(project_dir, 'Moonshot.uproject')

    if system == 'Windows':
        batch_files_path = os.path.join('Engine', 'Build', 'BatchFiles')
        clean_script = os.path.join(UNREAL_PATH, batch_files_path, 'Clean.bat')
        build_script = os.path.join(UNREAL_PATH, batch_files_path, 'Build.bat')
        package_script = os.path.join(UNREAL_PATH, batch_files_path, 'RunUAT.bat')
        platform_name = 'Win64'
    
    elif system == 'Darwin':  # macOS
        batch_files_path = os.path.join('Engine', 'Build', 'BatchFiles', 'Mac')
        clean_script = os.path.join(UNREAL_PATH, batch_files_path, 'Clean.sh')
        build_script = os.path.join(UNREAL_PATH, batch_files_path, 'Build.sh')
        package_script = os.path.join(UNREAL_PATH, batch_files_path, 'Package.sh')
        platform_name = 'Mac'
    
    else:   # Linux
        print("TODO: Linux")

    if clean:
        print(f"Cleaning {build_type} target with Unreal Engine at {UNREAL_PATH}")
        subprocess_list = [
            clean_script,
            target_name,
            platform_name,
            build_type,
            project_path,
            '-waitmutex'
        ]

    if build:
        print(f"Building {build_type} target with Unreal Engine at {UNREAL_PATH}")
        subprocess_list = [
            build_script,
            target_name,
            platform_name,
            build_type,
            project_path,
            '-waitmutex'
        ]
    
    if package:
        if target_name == 'MoonshotEditor':
            raise Exception("Cannot package editor target")
        
        print(f"Packaging {build_type} target with Unreal Engine at {UNREAL_PATH}")
        subprocess_list = [
            package_script,
            'BuildCookRun',
            '-noP4',
            '-utf8output',
            '-cook',
            '-project={}'.format(project_path),
            '-target={}'.format(target_name),
            '-platform={}'.format(platform_name),
            '-stage',
            '-archive',
            '-package',
            '-build',
            '-clean',
            '-pak',
            '-iostore',
            '-prereqs',
            '-archivedirectory={}}'.format(os.path.join(project_path, ARCHIVE_DIRECTORY, platform.system())),
            '-manifests',
            '-nocompileuat',
            '-waitmutex'
        ]

    subprocess.check_call(subprocess_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build commands for Moonshot project")

    parser.add_argument('--project-dir', type=str, required=True,
                        help="Path to the Moonshot project directory")
    parser.add_argument('--build-type', type=str, required=True,
                        help="Type of build (debug, development, testomg. release)")
    parser.add_argument('--target-name', type=str, required=True,
                        help="Type of build (debug, development, testomg. release)")
    parser.add_argument('--clean', action='store_true',
                        help="Clean selected targets")
    parser.add_argument('--build', action='store_true',
                        help="Build selected targets")
    parser.add_argument('--package', action='store_true',
                        help="Package selected target for deployment")
    
    args = parser.parse_args()

    build_project(
        build_type=args.build_type,
        target_name=args.target_name,
        project_dir=args.project_dir,
        build=args.build,
        clean=args.clean,
        package=args.package
        )
    
    
    