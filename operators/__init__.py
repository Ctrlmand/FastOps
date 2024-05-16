from .. import utility
from . import object_material, object_modifier, Image_switch_channel, node_merge_tex_channel, object_edit_normal, object_rename, object_select, node_change_colorspace, obj_move_to_collection_by_name, window_switch_ui_type
submod=[
    object_rename,
    object_select,
    object_edit_normal,
    node_change_colorspace,
    obj_move_to_collection_by_name,
    Image_switch_channel,
    node_merge_tex_channel,
    window_switch_ui_type,
    object_modifier,
    object_material,
]
_modcls=[]
for mod in submod:
    _modcls += mod._cls

# Register Functin
def register():
    utility.register_list.Register("OT", _modcls)
def unregister():
    utility.register_list.Unregister("OT", _modcls)