import os
import glob
from importlib import import_module

# Automatically import all .py files in this directory
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if os.path.isfile(f) and not f.endswith('__init__.py')]

for module in __all__:
    globals()[module] = import_module(f".{module}", package=__name__)