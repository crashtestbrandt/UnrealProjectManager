# Unreal Project Manager (UPM)

A lightweight Python module for managing Unreal projects across space, time, and platforms.

**Who it's for:**

Less-than-professional teams working with Git and VS Code.

**How to get:**

 - [UPM on PyPi](https://pypi.org/project/unreal-project-manager/):

    ```
    pip install unreal-project-manager
    ```

- [UPM on GitHub](https://github.com/crashtestbrandt/UnrealProjectManager):

    ```
    git clone https://github.com/crashtestbrandt/UnrealProjectManager
    ```

## Features

- Platform-aware generation of VS Code tasks to cook, build, package, and launch your Unreal 5+ project without having to open the editor (or just use the UPM CLI).

- Projects can be cloned and set up for Windows, Mac, or Linux environments from a single config file with sane defaults.

- Central management of project/package versioning and patch notes.

- CLI commands for installing build dependencies and tools.

- UPM can self-copy itelf into existing repositories so there's no need to mess with submodules or forking.

## Contents

- [Prerequisites](#prerequisites)

- [Quickstart](#quickstart)

- [UPM Config](#upm-config)

- [UPM Setup](#upm-setup)

- [Usage](#usage)

    - [Build and Launch](#build-and-launch)

    - [Changelog](#changelog)

- [Collaboration Guide](#collaboration-guide)

- [Also Maybe Helpful](#also-maybe-helpful)

    - [Installing Python](#installing-python)

    - [Installing Unreal](#installing-unreal)

    - [Starting an Unreal Project](#starting-an-unreal-project)

## Prerequisites

- [Python 3.10+](#installing-python)

- [Unreal Engine 5+](#installing-unreal)

## Quickstart

1. Download and install [prerequisites](#prerequisites).

1. Install UPM:

    `python3 -m pip install unreal-project-manager`

1. Use UPM to configure your project:

    `python3 -m upm config --dir [project-path] --project-name [project-name]`

1. Use UPM to install build tools.

    - For Windows, install Visual Studio Community with `python3 -m upm install-vs`. This will prompt for privilege escalation.

    - For MacOS, install XCode with `python3 -m upm install-xcode` (STILL TESTING)

    Additionally, if you don't have VS Code installed, you can do:

    `python3 -m upm install-vscode`

1. Navigate to your project directory and use UPM to perform project setup and generate project files:

    `python3 -m upm setup`

1. With your new *.code-workspace* file open in VS Code, use *Ctrl+Shift+B* to open the build menu and build your project.

    To fully cook, build, and package a development version of your project, choose the *Development Package* option. This is required before launching the *Development* configuration for your game from the Run and Debug menu (*Ctrl+Shift+D*), as building and launching a *Development* target directly will result in shaders not being compiled.

    To work on your project in the editor, first select the *Select-A-Build* option from the build menu, selecting the *Development* and *Editor* options when prompted.

1. Once your chosen target is built, navigate to the Run and Debug menu (*Ctrl+Shift+D*), select the target to launch from the dropdown menu, and click *Start Debugging* (green arrow). If this is your first time launching the Editor for your project, be prepared for it to hang a while as it compiles shaders.


## UPM Config

Adds scripts and configuration files to your project you'll probably want to keep under source control for use by collaborators. 

### Generate Configuration Files

**NOTE**: Here we're using Epic's [Lyra Starter Game](https://www.unrealengine.com/marketplace/en-US/product/lyra?sessionInvalidated=true) sample as an example project.

1. Install UPM:

    ```
    python3 -m pip install unreal-project-manager
    ```

1. Use UPM to copy configuration files into your project directory:

    ```
    python3 -m upm config --dir ../LyraStarterGame
    ```

    This creates several items in your target directory:

    - *config.upm*: Contains UPM project configuration values `upm setup` uses to generate UPM project files and VS Code tasks.

    - *Changelog.json*: Used by `upm changelog` to centralize patch notes (initialized with version *0.0.0-Alpha*; modify this as you see fit). 

    - *upm/*: Directory containing UPM scripts used by generated VS Code tasks for build/cook/launch/package/deploy/change automation.

    - *.gitignore*: Default .gitignore file for use with Unreal 5+, C++, Python 3.10+, and UPM. Omit this argument if you already have a suitable .gitignore file in the target directory.

### Configuration Options

If *config.upm* already exists in your project directory, UPM won't overwrite it. This allows you to keep a default *config.upm* under version control for your project. If you choose to do this but end up occasionally requiring a non-default *config.upm*, you can copy you custom *config.upm* into the *.vscode* directory of your project (which is ignored by the default .gitignore); `upm setup` will look here first for a config file.

To remove items created by `upm config`, do `upm config --clean --dir your-project-dir/`.

Do `upm config -h` to see options for modifying the default behavior of `upm config`, e.g. changing the default location of Unreal Engine or specifying a project name different from the project directory.

## UPM Setup

Generates files required for project automation, including Python dependencies (installed to *.venv* by default), environment variables (*.env* by default), VS Code workspace configuration files, build/launch tasks, and Unreal project files. These are all excluded via the default *.gitignore* file added by `upm config`.

To set up your project with UPM:

1. Ensure you've configured it using `upm config` as discussed in previous sections.

1. Ensure build tools are installed for your platform, e.g. by doing `python3 -m upm install-vs`.

1. Navigate to your project directory and do:

    ```
    python3 -m upm setup
    ```

The files and directories generated by `upm setup` are not intended to be placed under source control. When [sharing your project for collaboration](#collaboration-guide), you should include instructions for generating them with UPM.

You can remove UPM files generated by `upm setup` with `upm setup --clean`; this does not remove Unreal project files or the *.code-workspace* file.

## Usage

###  Build and Launch

UPM adds several platform-specific tasks to `.vscode/launch.json` and `.vscode/tasks.json`, which are wrappers for the various `upm build` commands:

![Build Task List](https://raw.githubusercontent.com/crashtestbrandt/UnrealProjectManager/main/images/build-task-list.png)

![Launch Target List](https://raw.githubusercontent.com/crashtestbrandt/UnrealProjectManager/main/images/launch-target-list.png)

```
usage: upm build [-h] --project-dir PROJECT_DIR --build-type BUILD_TYPE --target-name TARGET_NAME [--clean] [--build] [--package]

options:
  -h, --help            show this help message and exit
  --project-dir PROJECT_DIR
                        Path to the project directory
  --build-type BUILD_TYPE
                        Type of build (debug, development, testing. release)
  --target-name TARGET_NAME
                        Name of target to build.
  --clean               Clean selected targets
  --build               Build selected targets
  --package             Package selected target for deployment
```

You can access the launch configurations from the Run and Debug menu (*Ctrl+Shift+D*) and the build tasks from the Build menu (*Ctrl+Shift+B*). You must build a target before launching it, i.e. use *Select-A-Build* from the Build menu before launching from the Run and Debug menu.

### Changelog

To create a changelog file with an initial version (0.0.1), do 


## Collaboration Guide

## Also Maybe Helpful

### Installing Python

**Windows**

To initiate Python 3 installation on Windows, open Powershell and do:

```
python3
```

This opens the Microsoft Store and prompts you install Python 3.12.

### Installing Unreal

### Starting an Unreal Project


