import os
import importlib
from bpy.types import Context
from .. import function
from ..function.classes import Operator
from ..function.debug import PrintInfo
from ..function import getStaticVar

import bpy
# ------------------------------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------------------------

# test operator
class F_OT_TEST(Operator):
    """"Test Operator"""
    bl_idname = "object.f_test"
    bl_label = "Test"
    bl_options = {'REGISTER', 'UNDO'}

    info: getStaticVar.get_modifier_enum() # type: ignore

    def execute(self, context: Context):
        # i = 0
        # self.Log(f"{i} objects finished")
        # self.Warning("Warning")
        # self.Error("Error")

        PrintInfo(bpy.data.meshes[1].name)
        return {'FINISHED'}


_modcls+=[F_OT_TEST]

# Register Functions
def register():
    function.utils.Register("OT", _modcls)
def unregister():
    function.utils.Unregister("OT", _modcls)
