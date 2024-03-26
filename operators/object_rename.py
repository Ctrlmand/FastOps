from typing import Any, Set
import bpy
import re
from bpy.types import Context

#rename
bpy.types.Scene.FastOpsObjectBatchRename_namePrefix = bpy.props.StringProperty(name= "FastOpsRename NamePrefix", default="")
bpy.types.Scene.FastOpsObjectBatchRename_suffixNumber = bpy.props.IntProperty(name= "FastOpsRename SuffixNumber", default=3)
bpy.types.Scene.FastOpsObjectBatchRename_suffixStart = bpy.props.IntProperty(name= "FastOpsRename SuffixStart", default=0)
#add suffix
bpy.types.Scene.FastOpsObjectBatchRename_isOnlyAddSuffix = bpy.props.BoolProperty(name= "FastOpsRename IsOnlyAddSuffix",default=False)
bpy.types.Scene.FastOpsObjectBatchRename_addSuffix = bpy.props.StringProperty(name= "FastOpsRename SetSuffix", default="")
#find and replace
bpy.types.Scene.FastOpsObjectBatchRename_find = bpy.props.StringProperty(name= "FastOpsRename Find", default= "")
bpy.types.Scene.FastOpsObjectBatchRename_replace = bpy.props.StringProperty(name= "FastOpsRename Replace", default= "")


class F_OT_ObjectBatchRename(bpy.types.Operator):
    """Batch Rename"""
    bl_idname = "object.fastops_batch_rename"
    bl_label = "Batch Rename"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        prefix = context.scene.FastOpsObjectBatchRename_namePrefix
        suffix_start = context.scene.FastOpsObjectBatchRename_suffixStart
        suffix_number = context.scene.FastOpsObjectBatchRename_suffixNumber
        suffix = context.scene.FastOpsObjectBatchRename_addSuffix
        is_only_suffix = context.scene.FastOpsObjectBatchRename_isOnlyAddSuffix

        # 1.general rename
        if not is_only_suffix:
            count=0
            # 2.traversal
            for index, obj in enumerate(context.selected_objects):
                # 3.index offset
                index += suffix_start
                # 4.rename
                obj.name = f"{prefix}_{index:>0{suffix_number}d}{suffix}"
                count=index+1
                ...
            # 5.report changed object's count
            self.report({'INFO'}, f"{count} objects renamed")

        # 6.only add suffix
        else:
            count=0
            for obj in context.selected_objects:
                obj.name = f"{obj.name}{suffix}"
                count+=1
                ...
            # 7.report changed object's count
            self.report({'INFO'}, f"{count} objects renamed")
        return {'FINISHED'}

class F_OT_SetMeshName(bpy.types.Operator):
    """Set Mesh Name"""
    bl_idname = "object.fastops_set_mesh_name"
    bl_label = "Set Mesh Name"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        # alias
        object = context.selected_objects
        # count
        cout=0
        empty_cout=0
        # 1.set mesh name
        for obj in object:
            # 2.ignore empty object
            if obj.type == "EMPTY":
                empty_cout+=1
                continue
            # 3.set name
            obj.data.name = obj.name
            cout+=1
            ...
        # 4.report changed object's count
        self.report({'INFO'}, f"{cout} mesh changed,{empty_cout} objects ignored")
        return {'FINISHED'}

class F_OT_FindAndReplace(bpy.types.Operator):
    """Replace Object Name"""
    bl_idname = "object.fastops_find_and_replace"
    bl_label = "Find And Replace Object Name"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        pattern = context.scene.FastOpsObjectBatchRename_find
        replace = context.scene.FastOpsObjectBatchRename_replace

        count=0
        # 1.traversal
        for index, obj in enumerate(context.selected_objects):
            # 2.edit name
            obj.name = re.sub(pattern, replace, obj.name)
            # old
            # obj.name = obj.name.replace(pattern, replace)
            count=index
            ...
        self.report({'INFO'}, f"{count}object name changed")
        ...
        return {'FINISHED'}

class F_OT_RenameByActiveMaterialName(bpy.types.Operator):
    """Rename by active material name"""
    bl_idname = "object.fastops_rename_by_active_material_name"
    bl_label = "Rename By Active Material Name"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        # scene property
        suffix_number = context.scene.FastOpsObjectBatchRename_suffixNumber
        suffix_start = context.scene.FastOpsObjectBatchRename_suffixStart
        # alias
        selected = bpy.context.selected_objects
        # variable
        mat_name_list =[]
        obj_name_list =[]
        empty_cout=0
        changed_count=0

        # 1.get selected objects active material name by traversal
        for obj in selected:
            # 1.if obj not mesh
            if obj.type != "MESH":
                empty_cout+=1
                continue
            mat_name_list.append(obj.active_material.name)
        # 2.convert to set
        mat_name_set = set(mat_name_list)
        #debug
        print(f"\033[33m >> material set: << \033[0m")
        print(f"\033[32m (mat):{mat_name_set} \033[0m ")
        # 3.get object list
        for mat_name in mat_name_set:
            # 4.find obj in scene
            for obj in bpy.data.objects:
                # 5.ignore other type
                if obj.type != "MESH" or obj.active_material == None:
                    continue
                # 6.if have same material
                if obj.active_material.name == mat_name:
                    # 7.store in list
                    obj_name_list.append(obj.name)
                    # print(f"\033[32m >> {obj.name} << \033[0m")
        # debug
        print(f"\033[33m >> object list: << \033[0m ")
        print(f"\033[32m (object):{obj_name_list} \033[0m ")
        # 8.rename object
        remove_obj_name=[]
        # mat
        for mat_name in mat_name_set:
            name_count=suffix_start # start with each mat
            # obj
            for obj_name in obj_name_list:
                # if slots[0] == mat_name : rename and store objects
                if mat_name == bpy.data.objects[obj_name].material_slots[0].name:
                    # obj name is same as changed name
                    remove_obj_name.append(obj_name)
                    if bpy.data.objects[obj_name].name == f"{mat_name}.{name_count:>0{suffix_number}}":
                        name_count+=1
                        empty_cout+=1
                        continue
                    else:
                        bpy.data.objects[obj_name].name = f"{mat_name}.{name_count:>0{suffix_number}}"
                        name_count+=1
                        changed_count+=1
                        # debug
                        print(f"\033[33m >> {mat_name}:{obj_name} << \033[0m ")
                        print(f"\033[32m suffix count:{name_count} \033[0m ")
                        
            # from origin list remove renamed object list
            obj_name_list = list(set(obj_name_list) - set(remove_obj_name))
        # 9.report info
        self.report({'INFO'}, f"{changed_count} object renamed, {empty_cout} objects ignored")
        return {'FINISHED'}
    
_cls=[
    F_OT_ObjectBatchRename,
    F_OT_SetMeshName,
    F_OT_FindAndReplace,
    F_OT_RenameByActiveMaterialName,
]