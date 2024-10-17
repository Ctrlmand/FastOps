import bpy
import re
from typing import Any, Set
from bpy.types import Context
from ..utility.base_class import Operator
from ..utility.debug import InfoOut, LabelOut, TitleOut
from ..utility.varis import ObjType

# F_OT_ObjectBatchRename
## rename
bpy.types.Scene.F_ObjectBatchRename_namePrefix = bpy.props.StringProperty(name= "F_Rename_Object NamePrefix", default="")
bpy.types.Scene.F_ObjectBatchRename_suffixNumber = bpy.props.IntProperty(name= "F_Rename_Object SuffixNumber", default=3)
bpy.types.Scene.F_ObjectBatchRename_suffixStart = bpy.props.IntProperty(name= "F_Rename_Object SuffixStart", default=0)
## add suffix
bpy.types.Scene.F_ObjectBatchRename_isOnlyAddSuffix = bpy.props.BoolProperty(name= "F_Rename_Object IsOnlyAddSuffix",default=False)
bpy.types.Scene.F_ObjectBatchRename_addSuffix = bpy.props.StringProperty(name= "F_Rename_Object SetSuffix", default="")

class F_OT_ObjectBatchRename(Operator):
    """Batch Rename"""
    bl_idname = "object.f_batch_rename"
    bl_label = "Batch Rename"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        prefix = context.scene.F_ObjectBatchRename_namePrefix
        suffix_start = context.scene.F_ObjectBatchRename_suffixStart
        suffix_number = context.scene.F_ObjectBatchRename_suffixNumber
        suffix = context.scene.F_ObjectBatchRename_addSuffix
        is_only_suffix = context.scene.F_ObjectBatchRename_isOnlyAddSuffix

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
            self.Log(f"{count} objects renamed")

        # 6.only add suffix
        else:
            count=0
            for obj in context.selected_objects:
                obj.name = f"{obj.name}{suffix}"
                count+=1
                ...
            # 7.report changed object's count
            self.Log(f"{count} objects renamed")
            
        bpy.ops.object.f_set_mesh_name()
        return {'FINISHED'}

class F_OT_SetMeshName(Operator):
    """Set Mesh Name"""
    bl_idname = "object.f_set_mesh_name"
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
        self.Log(f"{cout} mesh changed,{empty_cout} objects ignored")
        return {'FINISHED'}

# F_OT_FindAndReplace
bpy.types.Scene.FastOpsObjectBatchRename_find = bpy.props.StringProperty(name= "F_Rename_Object Find", default= "")
bpy.types.Scene.FastOpsObjectBatchRename_replace = bpy.props.StringProperty(name= "F_Rename_Object Replace", default= "")

class F_OT_FindAndReplace(Operator):
    """Replace Object Name"""
    bl_idname = "object.f_find_and_replace"
    bl_label = "Find And Replace Object Name"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        pattern = context.scene.FastOpsObjectBatchRename_find
        replace = context.scene.FastOpsObjectBatchRename_replace

        count=0
        # 1.traversal
        for obj in context.selected_objects:
            # 2.edit name
            if pattern in obj.name:
                obj.name = re.sub(pattern, replace, obj.name)
                count+=1
            ...
        self.Log(f"{count}object name changed")
        ...
        return {'FINISHED'}

class F_OT_RenameByActiveMaterialName(Operator):
    """Rename by active material name"""
    bl_idname = "object.f_rename_by_active_material_name"
    bl_label = "Rename By Active Material"
    bl_options = {'REGISTER', 'UNDO'}

    # is_only_obj: bpy.props.BoolProperty(name="Is Only Object", default=False)# type:ignore
    set_mesh_name: bpy.props.BoolProperty(name="Set Mesh Name", default=True)# type:ignore

    def execute(self, context: Context):

        # scene property
        suffix_number = context.scene.F_ObjectBatchRename_suffixNumber
        suffix_start = context.scene.F_ObjectBatchRename_suffixStart
        # is_only_obj = self.is_only_obj

        # alias
        selected = bpy.context.selected_objects
        # variable
        mat_name_list=[]
        obj_name_list=[]
        ignore_cout=0
        changed_count=0

        # 1.get selected objects active material name by traversal
        for obj in selected:
            # make sure obj and mat is ok
            if obj.type != "MESH":
                ignore_cout+=1
                continue
            if obj.active_material == None:
                continue
            # get selected mat list
            mat_name_list.append(obj.active_material.name)
        # convert to set
        mat_name_set = set(mat_name_list)

        # 3.get obj list
        for obj in bpy.data.objects:
            # make sure obj ok
            if obj.type != "MESH" or obj.active_material == None:
                continue
            # if have same material
            if obj.active_material.name in mat_name_set:
                # 6.store to list
                obj_name_list.append(obj.name)

        # 8.rename object
        # mat
        for mat_name in mat_name_set:
            TitleOut(mat_name)          
            # start with each mat
            name_count=suffix_start 

            # obj
            for obj_name in obj_name_list:
                # start with each obj
                if not obj_name in bpy.data.objects.keys():
                    continue
                obj = bpy.data.objects.get(obj_name)
                if obj.type != ObjType.MESH:
                    continue

                # obj active_mat is mat 
                if mat_name == obj.active_material.name:
                    # obj's mat has only one user
                    if bpy.data.materials.get(mat_name).users == 1:
                        LabelOut("Only One User")
                        obj.name = mat_name
                        changed_count+=1
                        break

                    new_name = f"{mat_name}.{name_count:>0{suffix_number}}"
                    # obj name is same as changed name
                    if bpy.data.objects[obj_name].name == new_name:
                        name_count+=1
                        ignore_cout+=1
                        continue
                    else:
                        bpy.data.objects[obj_name].name = new_name
                        name_count+=1
                        changed_count+=1
                        
                    # in view layer-select
                    if obj_name in bpy.context.view_layer:
                        bpy.data.objects[obj_name].select_set(True)

        # set mesh name
        bpy.ops.object.f_set_mesh_name()

        # 9.report info
        if changed_count == 0 and ignore_cout == 0:
            self.Warning(f"Nothing changed")
        else:
            self.Log(f"{changed_count} object renamed, {ignore_cout} objects ignored")

        return {'FINISHED'}
    def invoke(self, context: Context, event):
        # wm = context.window_manager
        # return wm.invoke_props_dialog(self)
        return self.execute(context)

bpy.types.Scene.F_EditMaterialNameInSelectedObjects_namePrefix = bpy.props.StringProperty(name="F_Rename_Material Prefix", default="")

class F_OT_EditMaterialNameInSelectedObjects(Operator):
    """Edit Material Name In Selected Objects"""
    bl_idname = "object.f_edit_material_name_in_selected_objects"
    bl_label = "Edit Material Name In Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}
    

    def execute(self, context: Context):
        prefix= context.scene.F_EditMaterialNameInSelectedObjects_namePrefix
        ignore=0

        p = re.compile(f"{prefix}")

        mat_set = set(context.object.material_slots.keys())
        for mat in mat_set:
            if p.match(f"{mat}"):
                ignore +=1
                continue
            else:
                bpy.data.materials[mat].name = f"{prefix}{bpy.data.materials[mat].name}"

        self.Log(f"{len(mat_set)-ignore} materials renamed, {ignore} materials ignored")
        return {'FINISHED'}
    # def invoke(self, context: Context, event):

    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)


_cls=[
    F_OT_ObjectBatchRename,
    F_OT_SetMeshName,
    F_OT_FindAndReplace,
    F_OT_RenameByActiveMaterialName,
    F_OT_EditMaterialNameInSelectedObjects,
]