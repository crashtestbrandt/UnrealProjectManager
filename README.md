# Unreal Project Manager (UPM)

A lightweight Python module for managing Unreal projects across space, time, and platforms.

## Features

- Platform-aware generation of VS Code tasks to build, launch, cook, and package your Unreal 5+ project without having to open the editor.

- Projects can be set up for Windows, Mac, and Linux environments from a single config file with sane defaults.

- Central management of project/package versioning and patch notes.

- CLI for managing all build dependencies and tools.

- UPM can self-copy itself into existing repositories so there's no need to mess with submodules.

## Contents

- [Prerequisites](#prerequisites)

- [Quickstart](#quickstart)

- [Configuration](#configuration)

- [Setup](#setup)

- [Usage](#usage)

- [Also Maybe Helpful](#also-maybe-helpful)

    - [Installing Python](#installing-python)

    - [Installing Unreal](#installing-unreal)

    - [Starting an Unreal Project](#starting-an-unreal-project)

## Prerequisites

- [Python 3.10+](#installing-python)

- [Unreal Engine 5+](#installing-unreal)

## Quickstart

1. Download and install [prerequisites](#prerequisites).

1. Clone UPM:

    **TODO**: This will be replaced with `pip install`.

    `git clone https://github.com/crashtestbrandt/UnrealProjectManager.git`

1. Navigate to cloned UPM directory and use UPM to configure your project:

    `upm config --dir [project-path] --project-name [project-name]`

1. Navigate to your project directory and use UPM to perform project setup and generate project files:

    `upm setup`

1. 


## Configuration

### Generate Configuration Files

**NOTE**: Here we're using Epic's [Lyra Starter Game](https://www.unrealengine.com/marketplace/en-US/product/lyra?sessionInvalidated=true) sample as an example project, and assuming you've [created it](#starting-an-unreal-project) in the same directory where you cloned *UnrealProjectManager*.

1. Clone UPM and navigate to it:

    **TODO**: This will be replaced with installation instructions using `pip`. 
    
    ```
    git clone https://github.com/crashtestbrandt/UnrealProjectManager.git
    cd UnrealProjectManager
    ```

1. Copy configuration files into your project directory:

    ```
    python3 -m upm config --gitignore --dir ../LyraStarterGame
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

## Setup



### Existing Unreal Project

*TODO*

### New Unreal Project

*TODO*

## Usage

*TODO*

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


