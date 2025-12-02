from typing import Set
import bpy
import re
from bpy.types import Context
from ..function.classes import Operator


class F_OT_ObjMoveToCollectionByName(Operator):
    """Move Objects to Collection by Name"""
    bl_idname = "object.f_obj_move_collection_by_name"
    bl_label = "Move Objects To Collection By Name"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        # alias
        context = bpy.context
        objects = bpy.context.selected_objects
        collection_data = bpy.data.collections
        
        # variable
        parent_collection_name = "Group"

        # make sure parent collection exist
        if not parent_collection_name in collection_data:
            bpy.data.collections.new(name=parent_collection_name)
            bpy.data.collections[parent_collection_name].color_tag = 'COLOR_05'
            context.scene.collection.children.link(bpy.data.collections[parent_collection_name])

        # 1.traversal
        for obj in objects:
            # 2.get prefix
            name_tmp = re.search(r'(?P<prefix>[A-Za-z_]+)(?P<suffix>_[\w+])', obj.name)
            # error handel
            if name_tmp == None:
                self.Error(f"{obj.name} does not have prefix")
                continue
            prefix = name_tmp.group('prefix')
            # 3.if collection not exist
            if not prefix in collection_data:
                # 4.creteate collection and link to parent collection
                bpy.data.collections.new(name=prefix)
                bpy.data.collections[prefix].color_tag = 'COLOR_02'
                bpy.data.collections[parent_collection_name].children.link(bpy.data.collections[prefix])
                ...
            # 5.move object to new collection 
            obj.users_collection[0].objects.unlink(obj)
            bpy.data.collections[prefix].objects.link(obj)
        return{'FINISHED'}
    
class F_OT_GenerateBasicLOD(Operator):
    """Auto Generate"""
    bl_idname = "object.f_obj_generate_basic_lod"
    bl_label = "Generate basic LOD"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for var in bpy.context.selected_objects:
            var.name = f"{var.name}_LOD0"
        bpy.ops.object.duplicate()
        for var in bpy.context.selected_objects:
            var.name = re.sub(r"_LOD0\.\d+$", "_LOD1", var.name)
            # context.view_layer.active_object = var
            var.modifiers.new("Decimate", "DECIMATE")
            var.modifiers[0].ratio = 0.5
        bpy.ops.object.duplicate()
        for var in bpy.context.selected_objects:
            var.name = re.sub(r"_LOD1\.\d+$", "_LOD2", var.name)
            var.modifiers[0].ratio = 0.25


        return{'FINISHED'}

_cls=[
    F_OT_ObjMoveToCollectionByName,
    F_OT_GenerateBasicLOD,

]