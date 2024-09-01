import os
import shutil

def upmcopy(args):
    print("Copying upm files...")
    upm_dir = os.path.dirname(__file__)
    upm_dir = os.path.abspath(upm_dir)
    upm_dir = os.path.normpath(upm_dir)
    print(f"upm_dir: {upm_dir}")
    shutil.copytree(upm_dir, os.path.join(args.dir, "upm"), dirs_exist_ok=True)
    print("upm files copied.")