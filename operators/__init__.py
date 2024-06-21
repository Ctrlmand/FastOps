import bpy
import os
import importlib
from bpy.types import Context
from .. import utility
from ..utility.base_class import Operator

# import submod
correct_dir = os.path.dirname(os.path.abspath(__file__))
py_files = [f[:-3] for f in os.listdir(correct_dir) if f.endswith(".py") and not f.startswith("__init__")]

submod=[]
for module_name in py_files:
    mod = importlib.import_module(f".{module_name}", package= "FastOps.operators")
    submod.append(mod)
# get _cls
_modcls=[]
for mod in submod:
    _modcls += mod._cls

# test operator

class F_OT_TEST(Operator):
    """"Test Operator"""
    bl_idname = "object.f_test"
    bl_label = "Test"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):
        i = 0
        self.Log(f"{i} objects finished")
        self.Warning("Warning")
        self.Error("Error")
    
        return {'FINISHED'}


_modcls+=[F_OT_TEST]

# Register Functin
def register():
    utility.register_list.Register("OT", _modcls)
def unregister():
    utility.register_list.Unregister("OT", _modcls)
