import os
import shutil
import json
import platform
from datetime import datetime

UNREAL_PATH_KEY = "UNREAL_PATH"
PROJECT_NAME_KEY = "PROJECT_NAME"
WORKSPACE_NAME_KEY = "WORKSPACE_NAME"
GAME_NAME_KEY = "GAME_NAME"
EDITOR_NAME_KEY = "EDITOR_NAME"
CHANGELOG_FILENAME_KEY = "CHANGELOG_FILENAME"

CONFIG_FILENAME = "config.upm"
GITIGNORE_SRCFILE = "gitignore.upm"
GITIGNORE_DSTFILE = ".gitignore"
UPM_DIR = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

def clean(args):
    upm_dir_path = os.path.join(args.dir, "upm")
    config_file_path = os.path.join(args.dir, CONFIG_FILENAME)
    gitignore_file_path = os.path.join(args.dir, GITIGNORE_DSTFILE)
    changelog_file_path = os.path.join(args.dir, args.changelog)

    # Remove the "upm" directory
    if os.path.exists(upm_dir_path):
        shutil.rmtree(upm_dir_path)
        print(f"Removed directory: {upm_dir_path}")
    else:
        print(f"Directory not found, skipping: {upm_dir_path}")

    # Remove the config file
    if os.path.exists(config_file_path):
        os.remove(config_file_path)
        print(f"Removed file: {config_file_path}")
    else:
        print(f"File not found, skipping: {config_file_path}")

    # Remove the .gitignore file
    if os.path.exists(gitignore_file_path):
        os.remove(gitignore_file_path)
        print(f"Removed file: {gitignore_file_path}")
    else:
        print(f"File not found, skipping: {gitignore_file_path}")

    # Remove the changelog file
    if os.path.exists(changelog_file_path):
        os.remove(changelog_file_path)
        print(f"Removed file: {changelog_file_path}")
    else:
        print(f"File not found, skipping: {changelog_file_path}")

    print(f"Config cleanup complete. Run 'upm setup --clean' from {args.dir} to remove generated setup files.")

def load_config_template(args):
    if args.file:
        with open(args.file, 'r') as f:
            return json.load(f)
    else:
        with open(os.path.join(UPM_DIR, CONFIG_FILENAME), 'r') as f:
            return json.load(f)

def config(args):
    if args.clean:
        clean(args)
        return

    shutil.copytree(
        UPM_DIR,
        os.path.join(args.dir, "upm"),
        dirs_exist_ok=True
        )
    print(f"Copied UPM scripts to {os.path.join(args.dir, 'upm')}")
    
    if not args.nogitignore:
        shutil.copy(
            os.path.join(UPM_DIR, GITIGNORE_SRCFILE),
            os.path.join(args.dir, GITIGNORE_DSTFILE)
        )
        print ("Copied .gitignore file.")
    else:
        print("Skipping .gitignore file.")
    
    config = load_config_template(args)

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
    
    if args.game_name:
        config[system][GAME_NAME_KEY] = args.game_name
    else:
        config[system][GAME_NAME_KEY] = config[system][PROJECT_NAME_KEY]
    
    if args.editor_name:
        config[system][EDITOR_NAME_KEY] = args.editor_name
    else:
        config[system][EDITOR_NAME_KEY] = f"{config[system][GAME_NAME_KEY]}Editor"

    if os.path.exists(os.path.join(args.dir, CONFIG_FILENAME)):
        print(f"Skipping create config file; UPM config file already exists at {os.path.join(args.dir, CONFIG_FILENAME)}")
    else:
        with open(os.path.join(args.dir, CONFIG_FILENAME), 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Created UPM config file at {os.path.join(args.dir, CONFIG_FILENAME)}")

    
    print(f"Configuration complete. Navigate to {args.dir} and run 'upm setup' to complete setup.")
    
