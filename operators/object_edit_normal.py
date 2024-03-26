from typing import Set
import bpy
from bpy.types import Context

class F_OT_AddSplitNormal(bpy.types.Operator):
    """Batch add split normal"""
    bl_idname = "object.fastops_add_split_normal"
    bl_label = "Add Split Normal"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        i=0
        for obj in context.selected_objects:
                if obj.type == 'MESH':
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.customdata_custom_splitnormals_add()
                    bpy.ops.object.mode_set(mode='OBJECT')
                    i+=1
        self.report({'INFO'}, f"{i} objects finished")
        return {"FINISHED"}

class F_OT_ClearSplitNormal(bpy.types.Operator):
    """Batch add split normal"""
    bl_idname = "object.fastops_clear_split_normal"
    bl_label = "Add Split Normal"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        i=0
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
                    bpy.ops.object.mode_set(mode='OBJECT')
                    i+=1
        self.report({'INFO'}, f"{i} objects' finished")
        return {"FINISHED"}

class F_OT_ClearSharp(bpy.types.Operator):
    """Batch clear sharp"""
    bl_idname = "object.fastpos_clear_sharp"
    bl_label = "Batch Clear Sharp"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):
        i=0
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.mark_sharp(clear=True)
                bpy.ops.object.mode_set(mode='OBJECT')
                i += 1
        self.report({'INFO'}, f"{i} objects finished")
        return {"FINISHED"}

_cls=[
    F_OT_AddSplitNormal,
    F_OT_ClearSplitNormal,
    F_OT_ClearSharp,
]