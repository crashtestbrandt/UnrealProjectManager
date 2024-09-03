import os
import shutil
import json
import platform
from datetime import datetime

UNREAL_PATH_KEY = "UNREAL_PATH"
PROJECT_NAME_KEY = "PROJECT_NAME"
WORKSPACE_NAME_KEY = "WORKSPACE_NAME"
CHANGELOG_FILENAME_KEY = "CHANGELOG_FILENAME"

CONFIG_FILENAME = "config.upm"
GITIGNORE_SRCFILE = "gitignore.upm"
GITIGNORE_DSTFILE = ".gitignore"
UPM_DIR = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

def load_config_template():
    with open(os.path.join(UPM_DIR, CONFIG_FILENAME), 'r') as f:
        return json.load(f)

def config(args):
    shutil.copytree(
        UPM_DIR,
        os.path.join(args.dir, "upm"),
        dirs_exist_ok=True
        )
    print(f"Copied UPM scripts to {os.path.join(args.dir, 'upm')}")
    
    if args.gitignore:
        shutil.copy(
            os.path.join(UPM_DIR, GITIGNORE_SRCFILE),
            os.path.join(args.dir, GITIGNORE_DSTFILE)
        )
        print ("Copied .gitignore file.")
    else:
        print("Skipping .gitignore file.")
    
    config = load_config_template()

    system = platform.system()

    if not (system == 'Windows' or system == 'Darwin'):
        system = 'Linux'
    
    if args.unreal:
        config[system][UNREAL_PATH_KEY] = args.unreal

    if args.project_name:
        config[system][PROJECT_NAME_KEY] = args.project_name
    else:
        config[system][PROJECT_NAME_KEY] = os.path.basename(args.dir)
    
    if args.workspace:
        config[system][WORKSPACE_NAME_KEY] = args.workspace
    else:
        config[system][WORKSPACE_NAME_KEY] = f"{os.path.basename(args.dir)}.code-workspace"

    if os.path.exists(os.path.join(args.dir, CONFIG_FILENAME)):
        print(f"Skipping create config file; UPM config file already exists at {os.path.join(args.dir, CONFIG_FILENAME)}")
    else:
        with open(os.path.join(args.dir, CONFIG_FILENAME), 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Created UPM config file at {os.path.join(args.dir, CONFIG_FILENAME)}")
    
    if os.path.exists(os.path.join(args.dir, args.changelog)):
        print(f"Skipping create changelog file; changelog file already exists at {os.path.join(args.dir, args.changelog)}")
    else:
        if args.changelog:
            config[system][CHANGELOG_FILENAME_KEY] = args.changelog
            changelog_stub = [{
                "Version": "0.0.0",
                "PrereleaseType": "Alpha",
                "ReleaseDate": datetime.now().strftime('%Y-%m-%d'),
                "Changes": [],
            }]
            with open(os.path.join(args.dir, args.changelog), 'w') as f:
                json.dump(changelog_stub, f, indent=4)
                print(f"Created changelog file with v.0.0.0 at {os.path.join(args.dir, args.changelog)}")
    
    print(f"Configuration complete. Navigate to {args.dir} and run 'upm setup' to complete setup.")
    
