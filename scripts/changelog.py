import json
import argparse
from datetime import datetime
import subprocess
import configparser
import os
import configparser
import shlex

import configparser

class CustomConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr  # Retain the original case

    def write(self, fp, spaces=False):
        """Write an .ini-format representation of the configuration state."""
        if spaces:
            delimiter = " = "
        else:
            delimiter = "="
        for section in self._sections:
            fp.write(f"[{section}]\n")
            for key, value in self._sections[section].items():
                if key != "__name__":
                    fp.write(f"{key}{delimiter}{value}\n")
            fp.write("\n")

PROJECT_DIR = './'
CHANGELOG_FILE = os.path.join(PROJECT_DIR, 'Changelog.json')
README_FILE = os.path.join(PROJECT_DIR, 'README.md')
INI_FILE_PATH = os.path.join(PROJECT_DIR, 'Config', 'DefaultGame.ini')

def load_changelog():
    with open(CHANGELOG_FILE, 'r') as file:
        return json.load(file)

def save_changelog(changelog):
    changelog[-1]['ReleaseDate'] = datetime.now().strftime('%Y-%m-%d')
    changelog[-1]['Commit'] = get_commit_hash()
    with open(CHANGELOG_FILE, 'w') as file:
        json.dump(changelog, file, indent=4)

def update_readme(changelog):
    with open(README_FILE, 'a') as file:
        entry = changelog[-1]
        version = entry.get('Version', 'Unknown')
        prerelease = entry.get('PrereleaseType', 'Release')
        prerelease = ""
        if 'PrereleaseType' in entry:
            prerelease = f" - {entry['PrereleaseType']}"
        release_date = entry.get('ReleaseDate', 'Unknown')
        commit = entry.get('Commit', 'Unknown')
        file.write(f"\n\n### Version {version} {prerelease}\n\n")
        file.write(f"**Release Date**: {release_date}\n\n")
        file.write(f"**Commit**: {commit}\n\n")
        file.write("**Changes**\n\n")
        for change in entry['Changes']:
            file.write(f"- {change}\n")

def get_commit_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode()

def increment_version(version):
    major, minor, patch = map(int, version.split('.'))
    patch += 1
    return f"{major}.{minor}.{patch}"

def add_version():
    changelog = load_changelog()
    latest_version = changelog[-1]['Version']
    new_version = increment_version(latest_version)
    new_entry = {
        "Version": new_version,
        "PrereleaseType": "Alpha",
        "ReleaseDate": datetime.now().strftime('%Y-%m-%d'),
        "Commit": get_commit_hash(),
        "Changes": []
    }
    changelog.append(new_entry)
    save_changelog(changelog)

def escape_input(user_input):
    return shlex.quote(user_input)

def add_change(change):
    changelog = load_changelog()
    changelog[-1]['Changes'].append(change)
    save_changelog(changelog)

def update_ini():
    changelog = load_changelog()
    config = CustomConfigParser(strict=False)
    config.read(INI_FILE_PATH)

    section = '/Script/EngineSettings.GeneralProjectSettings'
    if section in config:
        config[section]['ProjectVersion'] = changelog[-1]['Version']
    else:
        raise Exception(f"Section {section} not found in {INI_FILE_PATH}")

    # Read the original file content
    with open(INI_FILE_PATH, 'r') as file:
        original_content = file.readlines()

    # Write the updated content back to the file
    with open(INI_FILE_PATH, 'w') as file:
        section_found = False
        for line in original_content:
            if line.strip().startswith(f"[{section}]"):
                section_found = True
            if section_found and line.strip().startswith("ProjectVersion"):
                file.write(f"ProjectVersion={changelog[-1]['Version']}\n")
                section_found = False  # Only update the first occurrence
            else:
                file.write(line)

def main():
    parser = argparse.ArgumentParser(description='Manage changelog')
    parser.add_argument('--add-version', action='store_true', help='Add an incremented version to the changelog')
    parser.add_argument('--add-change', type=str, help='Add a change to the most recent version')
    parser.add_argument('--update-readme', action='store_true', help='Append changes to README.md')
    parser.add_argument('--update-ini', action='store_true', help='Copy the most recent version number Config/DefaultGame.ini')

    args = parser.parse_args()

    if args.add_version:
        add_version()
    if args.add_change:
        add_change(args.add_change)
    if args.update_readme:
        changelog = load_changelog()
        update_readme(changelog)
    if args.update_ini:
        update_ini()

if __name__ == '__main__':
    main()