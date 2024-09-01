import os
import argparse
from dotenv import load_dotenv

DOTENV_PATH = '.env'
UNREAL_PATH_KEY = 'UNREAL_PATH'

load_dotenv(DOTENV_PATH)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query project environment.")

    parser.add_argument('--unreal-path', action='store_true', help="Print the Unreal Engine path")

    args = parser.parse_args()

    if args.unreal_path:
        print(os.getenv(UNREAL_PATH_KEY))