import bpy
from ..utility.base_class import Operator
from bpy.types import Context


class F_OT_ClearScene(Operator):
    """Clear scene"""
    bl_idname = "object.f_clear_scene"
    bl_label = "Clear Scene"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        bpy.ops.object.hide_view_clear()
        for var in bpy.context.view_layer.objects:
            var.select_set(True)
        bpy.ops.object.delete(use_global=False)
        bpy.ops.outliner.orphans_purge()
        return{'FINISHED'}


_cls=[
    F_OT_ClearScene,

]