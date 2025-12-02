import os
import importlib
from ..function import utils

# import submod
correct_dir = os.path.dirname(os.path.abspath(__file__))
py_files = [f[:-3] for f in os.listdir(correct_dir) if f.endswith(".py") and not f.startswith("__init__")]

submod=[]
for module_name in py_files:
    mod = importlib.import_module(f".{module_name}", package= "FastOps.ui")
    submod.append(mod)
# get _cls
_modcls=[]
for mod in submod:
    _modcls += mod._cls

# Register Function
def register():
    utils.Register("UI", _modcls)
def unregister():
    utils.Unregister("UI", _modcls)