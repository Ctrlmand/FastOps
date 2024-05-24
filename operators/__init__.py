import bpy
from bpy.types import Context

from .. import utility
from ..utility import matching
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


class F_OT_Test(bpy.types.Operator):
    """"Test Operator"""
    bl_idname = "object.fastops_test"
    bl_label = "Test"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        lis=matching.match_obj(bpy.data.objects, "MESH")
        self.report({"INFO"}, f"{lis}")
        return {'FINISHED'}

# Register Functin
def register():
    utility.register_list.Register("OT", _modcls)
    utility.register_list.Register("OT", [F_OT_Test])
def unregister():
    utility.register_list.Unregister("OT", _modcls)
    utility.register_list.Unregister("OT", [F_OT_Test])