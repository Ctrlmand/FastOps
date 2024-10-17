from typing import Any, Set
import bpy
from bpy.types import Context
from ..utility.debug import P, InfoOut
from ..utility.matching import MatchObjectByPrefix
from ..utility.base_class import Operator
from ..utility.varis import ObjType

class F_OT_AddSplitNormal(Operator):
    """Batch add split normal"""
    bl_idname = "mesh.f_add_split_normal"
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
        self.Log(f"{i} objects finished")
        return {"FINISHED"}

class F_OT_ClearSplitNormal(Operator):
    """Batch add split normal"""
    bl_idname = "mesh.f_clear_split_normal"
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
        self.Log(f"{i} objects' finished")
        return {"FINISHED"}

class F_OT_ClearSharp(Operator):
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
        self.Log(f"{i} objects finished")
        return {"FINISHED"}

class F_OT_BatchAddUVLayer(Operator):
    """Batch add UV layer"""
    bl_idname = "mesh.f_batch_add_uv_layer"
    bl_label = "Batch Add UV Layer"
    bl_options = {'REGISTER', 'UNDO'}

    uv_name: bpy.props.StringProperty(name="UV Name", default="") # type: ignore

    def execute(self, context: Context):
        C=context
        
        for obj in C.selected_objects:
            if obj.data.uv_layers.get(self.uv_name) != None:
                 continue

            uvlayer_index = len(obj.data.uv_layers.keys())
            obj.data.uv_layers.new(name = self.uv_name)
            obj.data.uv_layers.active_index = uvlayer_index

        self.Log(f"UV layers added sucessfully!")

        return {"FINISHED"}
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "uv_name", text="UV Name")

class F_OT_GetMeshMatchedObjects(Operator):
    """Match mesh from high or low model"""
    bl_idname = "mesh.f_get_mesh_matched_objects"
    bl_label = "Get Mesh Matched Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):
        for obj in context.selected_objects:
            matched_obj = MatchObjectByPrefix(obj)

            # match sucess
            if matched_obj != None:
                # report
                self.Log(f"Success: matched {matched_obj.name}")

                new_mesh = bpy.data.meshes.new_from_object(matched_obj, preserve_all_data_layers=True)
                obj.data = new_mesh

            else:
                self.Warning(f"Failed: matched {matched_obj.name}")
                continue

            ...
        return {"FINISHED"}
    ...

_cls=[
    F_OT_AddSplitNormal,
    F_OT_ClearSplitNormal,
    F_OT_ClearSharp,
    F_OT_BatchAddUVLayer,
    F_OT_GetMeshMatchedObjects,
]