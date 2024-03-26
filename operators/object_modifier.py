from typing import Any
import bpy
from bpy.types import Context

class F_OT_AddModifier(bpy.types.Operator):
    """Batch Add Modifier To Selected Objects"""
    bl_idname = "object.fastops_clear_all_modifier"
    bl_idname = "object.fastops_quick_mirror"
    bl_label = "Modifier"
    bl_options = {'REGISTER', 'UNDO'}
    # enum property
    modifer_type: bpy.props.EnumProperty(
        name = "Modifier Type",
        description = "Modifier Type",
        default = 'MIRROR',
        items =(
            ('MIRROR', 'Mirror', 'Mirror'),
            ('SOLIDIFY', 'Solidify', 'Solidify'),
            ('BEVEL', 'Bevel', 'Bevel'),
            ('WEIGHTED_NORMAL', 'Weighted Normal', 'Weighted Normal'),
            ('DECIMATE', 'Decimate', 'Decimate'),
            ('ARRAY', 'Array', 'Array'),
            ('WELD', 'Weld', 'Weld'),
            ('SHRINKWRAP', 'Shrinkwrap', 'Shrinkwrap')
        ),
    ) # type: ignore

    def execute(self, context: bpy.types.Context):
        # alias
        active_object = bpy.context.active_object
        selected_objects = bpy.context.selected_objects
        # interation
        for obj in selected_objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_add(type = self.modifer_type)
        self.report({'INFO'}, f"{len(selected_objects)} Objects Added <{self.modifer_type}>")
        return {'FINISHED'}

class F_OT_ClearAllModifier(bpy.types.Operator):
    """Clear All Modifiers"""
    bl_idname = "object.fastops_clear_all_modifier"
    bl_label = "Clear All Modifiers"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        active_object = bpy.context.active_object
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            context.view_layer.objects.active = obj
            for mod in obj.modifiers:
                bpy.ops.object.modifier_remove(modifier=mod.name)

        self.report({'INFO'}, f"{len(selected_objects)} Objects Cleared; Modifiers Total:{len(obj.modifiers)}")
        return {'FINISHED'}
_cls=[
    F_OT_AddModifier,
    F_OT_ClearAllModifier
]