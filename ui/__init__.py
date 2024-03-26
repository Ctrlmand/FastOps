from .. import utility
from . import pie_View3D, ui_object_edit_normal, ui_object_rename, ui_object_select, ui_object_set_pass_id, ui_move_to_collection_by_name, ui_node_option
submod=[
    pie_View3D,
    ui_object_rename,
    ui_object_edit_normal,
    ui_object_set_pass_id,
    ui_object_select,
    ui_move_to_collection_by_name,
    ui_node_option
]
_modcls=[]
for mod in submod:
    _modcls += mod._cls

# Register Function
def register():
    utility.register_list.register("UI", _modcls)
def unregister():
    utility.register_list.unregister("UI", _modcls)