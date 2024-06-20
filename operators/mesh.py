from typing import Any, Set
import bpy
from bpy.types import Context

class F_OT_AddSplitNormal(bpy.types.Operator):
    """Batch add split normal"""
    bl_idname = "mesh.fastops_add_split_normal"
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
    bl_idname = "mesh.fastops_clear_split_normal"
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

bpy.types.Scene.F_MeshBatchAddUVLayer_name = bpy.props.StringProperty(name="F_Mesh_AddUVLayer_Name", default="")

class F_OT_BatchAddUVLayer(bpy.types.Operator):
    """Batch add UV layer"""
    bl_idname = "mesh.fastops_batch_add_uv_layer"
    bl_label = "Batch Add UV Layer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):
        C=context
        uv_name = context.scene.F_MeshBatchAddUVLayer_name
        
        for obj in C.selected_objects:
            uvlayer_index = len(obj.data.uv_layers.keys())-1
            obj.data.uv_layers.new(name = uv_name)
            obj.data.uv_layers.active_index = uvlayer_index

        self.report({'INFO'}, f"UV layers added sucessfully!")

        return {"FINISHED"}

_cls=[
    F_OT_AddSplitNormal,
    F_OT_ClearSplitNormal,
    F_OT_ClearSharp,
    F_OT_BatchAddUVLayer,
]