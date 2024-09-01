# UnrealProjectManager

Lightweight cross-platform tools to streamline build management and collaboration for small teams using VS Code.

## Features

- Platform-aware generation of VS Code tasks to build, launch, cook, and package your Unreal 5+ project without having to open the editor.

- Projects can be set up for Windows, Mac, and Linux environments from a single config file with sane defaults.

- Central management of project/package versioning and patch notes.

- CLI for downloading and installing all build dependencies and tools.

## Contents

- [Setup](#Setup)
- [Usage](#usage)
- [Also Maybe Helpful](#also-maybe-helpful)

## Setup

### Existing Unreal Project

### New Unreal Project

## Usage

```
Unreal Project Manager CLI

python -m upm {command}

    upm setup [-h] [--clean]        Run setup script.

        --clean                     Clean generated project files.

    build [-h] --project-dir PROJECT_DIR --build-type BUILD_TYPE --target-name TARGET_NAME [--clean] [--build] [--package]

        --project-dir PROJECT_DIR   Path to the Moonshot project directory
        --build-type BUILD_TYPE     Type of build (debug, development, testomg. release)
        --target-name TARGET_NAME   Type of build (debug, development, testomg. release)
        --clean                     Clean selected targets
        --build                     Build selected targets
        --package                   Package selected target for deployment
    
    install-vscode                  Download and install Visual Studio Code.
    install-vs                      Download and install Visual Studio Community (prompts for admin privileges).
    upmcopy [-h] --dir DIR          Copy upm files to a destination folder.
```

## Also Maybe Helpful


