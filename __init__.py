bl_info = {
    "name": "FastOps",
    "author": "shaoge",
    "version": (1, 0, 1),
    "blender": (4, 0, 0),
    "location": "View 3D",
    "description": "",
    "warning": "",
    "category": "3D View",
}

import bpy
from . import operators
from . import ui
from . import keymap
from .utility import register_list
# operator list
_cls = operators._modcls + ui._modcls
classes = _cls

def register():
    # Register Operator
    operators.register()
    
    # Register UI
    ui.register()

    # Registe keymap
    keymap.km_handle.register()
def unregister():
    # UnRegister Operator
    operators.unregister()
    
    # UnRegister UI
    ui.unregister()

    # Unregiste KeyMap
    keymap.km_handle.unregister()

if __name__ == "__main__":
    register()