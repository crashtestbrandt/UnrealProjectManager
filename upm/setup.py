import os
import platform
import subprocess
import sys
import json

PROJECT_NAME_KEY = "PROJECT_NAME"
GAME_NAME_KEY = "GAME_NAME"
EDITOR_NAME_KEY = "EDITOR_NAME"
WORKSPACE_NAME_KEY = "WORKSPACE_NAME"
UNREAL_PATH_KEY = "UNREAL_PATH"
CHANGELOG_FILENAME_KEY = "CHANGELOG_FILENAME"
VENV_DIR = ".venv"
DOTENV_FILE = '.env'
VSCODE_DIR = '.vscode'
CONFIG_PATH = os.path.join(os.getcwd(),'config.upm')
LAUNCH_TEMPLATE_PATH = os.path.join(os.getcwd(), 'upm', 'launch.upm')
TASKS_TEMPLATE_PATH = os.path.join(os.getcwd(), 'upm', 'tasks.upm')
REQUIREMENTS_FILE = 'requirements.txt'

UBT_SOURCE_PATH = os.path.join('Engine', 'Source', 'Programs', 'UnrealBuildTool')
UBT_EXEC_PATH = os.path.join('Engine', 'Binaries', 'DotNET', 'UnrealBuildTool', 'UnrealBuildTool.exe')

def create_virtualenv(venv_path):
    print(f'Creating virtual environment at {venv_path}...')
    if not os.path.exists(venv_path):
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        print(f'Created virtual environment at {venv_path}')
    else:
        print(f'Virtual environment already exists at {venv_path}')

def install_dependencies(venv_path, requirements_file):
    system = platform.system()

    if system == 'Windows':
        python_executable = os.path.join(venv_path, 'Scripts', 'python')
    elif system == 'Darwin':  # macOS
        python_executable = os.path.join(venv_path, 'bin', 'python3')
    else:  # Assuming Linux or other Unix-like OS
        python_executable = os.path.join(venv_path, 'bin', 'python3')

    subprocess.check_call([python_executable, '-m', 'pip', 'install', '-r', requirements_file])
    print(f'Installed dependencies from {requirements_file}')

def load_config(config_file):
    config = None
    with open(config_file, 'r') as f:
        config = json.load(f)

    system = platform.system()

    if not (system == 'Windows' or system == 'Darwin'):
        system = 'Linux'

    env_vars = config[system]


    with open(DOTENV_FILE, 'w') as env_file:
        for key, value in env_vars.items():
            env_file.write(f"{key}={value}\n")

    return env_vars

def create_launch_tasks(env_vars):
    # Ensure the .vscode directory exists
    vscode_dir = os.path.join(os.getcwd(), '.vscode')
    if not os.path.exists(vscode_dir):
        os.makedirs(vscode_dir)

    project_name = env_vars[PROJECT_NAME_KEY]

    system = platform.system()

    if system == 'Windows':
        editor_path = os.path.join(env_vars[UNREAL_PATH_KEY], 'Engine', 'Binaries', 'Win64', 'UnrealEditor.exe')
        exec_path = os.path.join(os.getcwd(), 'Binaries', 'Win64', f"{env_vars[GAME_NAME_KEY]}.exe")
        visualizer_path = os.path.join(env_vars[UNREAL_PATH_KEY], 'Engine', 'Extras', 'VisualStudioDebugging', 'Unreal.natvis')
        type_val = "cppvsdbg"
    elif system == 'Darwin':  # macOS
        editor_path = os.path.join(env_vars[UNREAL_PATH_KEY], 'Engine', 'Binaries', 'Mac', 'UnrealEditor.app', 'Contents', 'MacOS', 'UnrealEditor')
        exec_path = os.path.join(os.getcwd(), 'Binaries', 'Mac', f"{project_name}.app", 'Contents', 'MacOS', f"{env_vars[GAME_NAME_KEY]}")
        type_val = "lldb"
        visualizer_path = None
    else:  # Assuming Linux or other Unix-like OS
        editor_path = os.path.join(env_vars[UNREAL_PATH_KEY], 'Engine', 'Binaries', 'Linux', 'UnrealEditor')
        exec_path = os.path.join(os.getcwd(), 'Binaries', 'Linux', f"{project_name}")
        type_val = "lldb"
        visualizer_path = None
    
    launch_tasks = None
    with open(LAUNCH_TEMPLATE_PATH, 'r') as f:
        launch_tasks = json.load(f)

    launch_tasks['configurations'].append({
        "name": f"Launch {project_name}Editor (Development)",
        "request": "launch",
        "program": editor_path,
        "args": [
            os.path.join(os.getcwd(), f"{project_name}.uproject")
        ],
        "stopAtEntry": False,
        "console": "integratedTerminal",
        "type": type_val,
        "visualizerFile": visualizer_path,
        "sourceFileMap": {
            "D:\\build\\++UE5\\Sync": env_vars[UNREAL_PATH_KEY]
        }
    })

    launch_tasks['configurations'].append({
        "name": f"Launch {env_vars[GAME_NAME_KEY]} (Development)",
        "request": "launch",
        "program": exec_path,
        "stopAtEntry": False,
        "console": "integratedTerminal",
        "type": type_val,
        "visualizerFile": visualizer_path,
        "sourceFileMap": {
            "D:\\build\\++UE5\\Sync": env_vars[UNREAL_PATH_KEY]
        }
    })

    # Write the launch.json file
    with open(os.path.join(vscode_dir, 'launch.json'), 'w') as tasks_file:
        json.dump(launch_tasks, tasks_file, indent=4)

    print(f'Created launch tasks in {os.path.join(vscode_dir, "launch.json")}')
    return launch_tasks

def create_build_tasks(env_vars):
    # Ensure the .vscode directory exists
    vscode_dir = os.path.join(os.getcwd(), '.vscode')
    if not os.path.exists(vscode_dir):
        os.makedirs(vscode_dir)

    project_name = env_vars[PROJECT_NAME_KEY]

    build_script = os.path.join(os.getcwd(), 'upm', 'build.py')
    changelog_script = os.path.join(os.getcwd(), 'upm', 'changelog.py')

    system = platform.system()

    if system == 'Windows':
        python_cmd = os.path.join(os.getcwd(), VENV_DIR, 'Scripts', 'python')
        
        shell_cmd = 'powershell'
        prebuild_args = [
            "/c",
            f"{python_cmd} {changelog_script} --update-ini && {python_cmd} {changelog_script} --update-readme && copy {env_vars[CHANGELOG_FILENAME_KEY]} {os.path.join('.', 'Content', project_name, 'Data')}"
        ]
    elif system == 'Darwin':  # macOS
        python_cmd = os.path.join(os.getcwd(), VENV_DIR, 'bin', 'python')
        shell_cmd = 'sh'
        prebuild_args = [
            f"{python_cmd} {changelog_script} --update-ini && {python_cmd} {changelog_script} --update-readme && cp {env_vars[CHANGELOG_FILENAME_KEY]} {os.path.join('.', 'Content', project_name, 'Data')}"
        ]
    else:  # Assuming Linux or other Unix-like OS
        python_cmd = os.path.join(os.getcwd(), VENV_DIR, 'bin', 'python')
        shell_cmd = 'sh'
        prebuild_args = []

    build_tasks = None
    with open(TASKS_TEMPLATE_PATH, 'r') as f:
        build_tasks = json.load(f)

    build_tasks['tasks'].append({
        "label": f"{project_name} Select-A-Build",
        "group": "build",
        "command": python_cmd,
        "args": [
            build_script,
            "--build-type",
            '${input:buildType}',
            "--target-name",
            "${input:targetName}",
            "--project-dir",
            "${workspaceFolder}",
            "--build",
        ],
        "problemMatcher": "$msCompile",
        "type": "shell"
    })

    build_tasks['tasks'].append({
        "label": f"{project_name} Select-A-Clean",
        "group": "build",
        "command": python_cmd,
        "args": [
            build_script,
            "--build-type",
            '${input:buildType}',
            "--target-name",
            "${input:targetName}",
            "--project-dir",
            "${workspaceFolder}",
            "--clean",
        ],
        "problemMatcher": "$msCompile",
        "type": "shell"
    })

    build_tasks['tasks'].append({
        "label": f"{project_name} Development Package",
        "group": "build",
        "command": python_cmd,
        "args": [
            build_script,
            "--build-type",
            'Development',
            "--target-name",
            f"{env_vars[GAME_NAME_KEY]}",
            "--project-dir",
            "${workspaceFolder}",
            "--package",
        ],
        "problemMatcher": "$msCompile",
        "type": "shell"
    })

    build_tasks['tasks'].append({
        "label": "Changelog: Add Version",
        "type": "shell",
        "command": python_cmd,
        "args": [
            changelog_script,
            "--add-version"
        ],
        "group": "build",
        "problemMatcher": []
    })

    build_tasks['tasks'].append({
        "label": "Changelog: Add Change",
        "type": "shell",
        "command": python_cmd,
        "args": [
            changelog_script,
            "--add-change",
            "${input:changeDescription}"
        ],
        "group": "build",
        "problemMatcher": []
    })

    build_tasks['tasks'].append({
        "label": "Changelog: Update README",
        "type": "shell",
        "command": python_cmd,
        "args": [
            changelog_script,
            "--update-readme"
        ],
        "group": "build",
        "problemMatcher": []
    })

    build_tasks['tasks'].append({
        "label": "Changelog: Update INI",
        "type": "shell",
        "command": python_cmd,
        "args": [
            changelog_script,
            "--update-ini"
        ],
        "group": "build",
        "problemMatcher": []
    })

    build_tasks['tasks'].append({
        "label": "Changelog: Prebuild Updates",
        "type": "shell",
        "command": shell_cmd,
        "args": prebuild_args,
        "group": "build",
        "problemMatcher": []
    })

    build_tasks['inputs'].append({
        "id": "targetName",
        "type": "pickString",
        "description": "Choose target.",
        "default": f"{project_name}",
        "options": [
            env_vars[GAME_NAME_KEY],
            env_vars[EDITOR_NAME_KEY]
        ]
    })

    build_tasks['inputs'].append({
        "id": "buildType",
        "type": "pickString",
        "description": "Type of build.",
        "default": "Development",
        "options": [
            "Development",
            "Debug",
            "DebugGame",
            "Test",
            "Shipping"
        ]
    })

    build_tasks['inputs'].append({
        "id": "changeDescription",
        "type": "promptString",
        "description": "Enter the change description"
    })

    

    # Write the tasks.json file
    with open(os.path.join(vscode_dir, 'tasks.json'), 'w') as tasks_file:
        json.dump(build_tasks, tasks_file, indent=4)

    print(f'Created build tasks in {os.path.join(vscode_dir, "build.json")}')
    return build_tasks

def create_code_workspace(env_vars):
    project_name = env_vars[PROJECT_NAME_KEY]
    workspace_name = env_vars[WORKSPACE_NAME_KEY]

    system = platform.system()

    if system == 'Windows':
        native_codeproj = os.path.join(project_name, project_name + '.generated.sln')
    elif system == 'Darwin':  # macOS
        native_codeproj = None
    else:  # Assuming Linux or other Unix-like OS
       native_codeproj = None
    
    code_workspace = {
        "folders": [
            {
                "name": project_name,
                "path": "."
            },
            {
                "name": "UE5",
                "path": env_vars[UNREAL_PATH_KEY]
            }
        ],
        "settings": {
            "typescript.tsc.autoDetect": "off",
            "npm.autoDetect": "off",
            "search.exclude": {
               f"{VENV_DIR}/**": True
            }, 
            "python.analysis.exclude": [
                f"{VENV_DIR}/**"
            ],
            "dotnet.defaultSolution": native_codeproj
        },
        "extensions": {
            "recommendations": [
                "ms-vscode.cpptools",
                "ms-dotnettools.csharp",
                "ms-vscode.powershell",
                "ms-python.python",
                "ms-vscode.cpptools-extension-pack",
                "ms-dotnettools.csdevkit"
            ]
        }
    }

    # Write the workspace file
    workspace_file = os.path.join(os.getcwd(), f"{workspace_name}")
    with open(workspace_file, 'w') as fp:
        json.dump(code_workspace, fp, indent=4)

    print(f'Created workspace file in {workspace_file}')

    return code_workspace

def build_unreal_build_tool(env_vars):
    unreal_path = env_vars[UNREAL_PATH_KEY]
    ubt_proj_file = os.path.join(unreal_path, UBT_SOURCE_PATH, 'UnrealBuildTool.csproj')
    if not os.path.exists(unreal_path):
        raise Exception(f"Unreal Engine not found at {unreal_path}")
    if not os.path.exists(ubt_proj_file):
        raise Exception(f"UnrealBuildTool.csproj not found at {ubt_proj_file}")
    print(f"Building Unreal Build Tool from source using {ubt_proj_file}...")
    subprocess_list = [
        'dotnet',
        'build',
        ubt_proj_file,
        '-c',
        'Development', 
    ]
    try:
        subprocess.check_call(subprocess_list, cwd=os.path.join(unreal_path, UBT_SOURCE_PATH))
        print("Built Unreal Build Tool successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building Unreal Build Tool: {e}")
        sys.exit(1)

def generate_project_files(env_vars):
    unreal_path = env_vars[UNREAL_PATH_KEY]
    project_name = env_vars[PROJECT_NAME_KEY]

    project_filepath = os.path.join(os.getcwd(), f"{project_name}.uproject")

    system = platform.system()

    build_ubt = False
    if system == 'Windows':
        if not os.path.exists(os.path.join(unreal_path, UBT_EXEC_PATH)):
            build_ubt = True
    
    elif system == 'Darwin':  # macOS
        batch_files_path = os.path.join('Engine', 'Build', 'BatchFiles', 'Mac')
        ubt_script = os.path.join(unreal_path, batch_files_path, 'RunUBT.sh')
        if not os.path.exists(ubt_script):
            build_ubt = True
    
    else:   # Linux
        print("TODO: Linux")
    
    if build_ubt:
        print(f"Unreal Build Tool not found at {os.path.join(unreal_path, UBT_EXEC_PATH)}")
        build_unreal_build_tool(env_vars)
    
    print(f"Generating project files for {project_filepath} with Unreal Engine at {unreal_path} ...")
    subprocess_list = [
        os.path.join(unreal_path, UBT_EXEC_PATH),
        '-projectfiles',
        '-project={}'.format(project_filepath),
        '-game',
        '-engine',
        '-dotnet',
        '-vscode'
    ]

    subprocess.check_call(subprocess_list)
    print(f"Generated project files for {project_filepath}")

def clean_project(env_vars):
    system = platform.system()

    if system == 'Windows':
        rm_venv_list = ['powershell', '-Command', 'Remove-Item', '-Recurse', '-Force', VENV_DIR]
        rm_dotvenv_list = ['powershell', '-Command', 'Remove-Item', '-Force', DOTENV_FILE]
        rm_tasks_list = ['powershell', '-Command', 'Remove-Item', '-Force', os.path.join(VSCODE_DIR, 'tasks.json')]
        rm_launch_list = ['powershell', '-Command', 'Remove-Item', '-Force', os.path.join(VSCODE_DIR, 'launch.json')]
        rm_workspace_list = ['powershell', '-Command', 'Remove-Item', '-Force', f"{env_vars[PROJECT_NAME_KEY]}.code-workspace"]
    else:
        rm_venv_list = ['rm', '-rf', VENV_DIR]
        rm_dotvenv_list = ['rm', '-f', DOTENV_FILE] 
        rm_tasks_list = ['rm', '-rf', os.path.join(VSCODE_DIR, 'tasks.json')]
        rm_launch_list = ['rm', '-f', os.path.join(VSCODE_DIR, 'launch.json')]
        rm_workspace_list = ['rm', '-rf', f"{env_vars[PROJECT_NAME_KEY]}.code-workspace"]

    if os.path.exists(VENV_DIR):
        print(f"Removing {VENV_DIR}...")
        subprocess.check_call(rm_venv_list)
        print(f"Removed {VENV_DIR}")

    if os.path.exists(DOTENV_FILE):
        print(f"Removing {DOTENV_FILE}...")
        subprocess.check_call(rm_dotvenv_list)
        print(f"Removed {DOTENV_FILE}")

    if os.path.exists(os.path.join(VSCODE_DIR, 'tasks.json')):
        print(f"Removing {os.path.join(VSCODE_DIR, 'tasks.json')}...")
        subprocess.check_call(rm_tasks_list)
        print(f"Removed {os.path.join(VSCODE_DIR, 'tasks.json')}")

    if os.path.exists(os.path.join(VSCODE_DIR, 'launch.json')):
        print(f"Removing {os.path.join(VSCODE_DIR, 'launch.json')}...")
        subprocess.check_call(rm_launch_list)
        print(f"Removed {os.path.join(VSCODE_DIR, 'launch.json')}")

    #if os.path.exists(f"{env_vars[PROJECT_NAME_KEY]}.code-workspace"):
    #    print(f"Removing {env_vars[PROJECT_NAME_KEY]}.code-workspace...")
    #    subprocess.check_call(rm_workspace_list, shell=True)
    #    print(f"Removed {env_vars[PROJECT_NAME_KEY]}.code-workspace")

    print(f"Project cleaned; {env_vars[PROJECT_NAME_KEY]}.code-workspace still exists and can be overwritten with \'upm setup\' if needed.")

def setup(args):
    config_override_path = os.path.join(os.getcwd(), '.vscode', 'config.upm')

    if os.path.exists(config_override_path):
        env_vars = load_config(config_override_path)
    elif os.path.exists(CONFIG_PATH):
        env_vars = load_config(CONFIG_PATH)
    else:
        raise Exception(f"Could not find {CONFIG_PATH} or {config_override_path}")
    
    if args.clean:
        clean_project(env_vars)
        sys.exit(0)

    venv_path = os.path.join(os.getcwd(), '.venv')
    
    requirements_file = os.path.join(os.getcwd(), 'upm', 'requirements.txt')

    if not args.novenv and not os.path.exists(venv_path):
        print(f"No virtual environment found at {venv_path}.")
        create_virtualenv(venv_path)
    else:
        print(f"Skipping virtual environment creation.")
    
    if args.novenv:
        print(f"Skipping dependency installation.")
    else:
        install_dependencies(venv_path, requirements_file)
        
    if not args.noprojfiles:
        generate_project_files(env_vars);

    create_launch_tasks(env_vars)
    create_build_tasks(env_vars)
    create_code_workspace(env_vars)
