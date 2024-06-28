import bpy
import re
from typing import Any, Set
from bpy.types import Context
from ..utility.base_class import Operator
from ..utility.debug import P

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

    is_only_obj: bpy.props.BoolProperty(name="Is Only Object", default=False)# type:ignore
    set_mesh_name: bpy.props.BoolProperty(name="Set Mesh Name", default=True)# type:ignore

    def execute(self, context: Context):
        # scene property
        suffix_number = context.scene.F_ObjectBatchRename_suffixNumber
        suffix_start = context.scene.F_ObjectBatchRename_suffixStart
        is_only_obj = self.is_only_obj
        set_mesh_name = self.set_mesh_name

        # alias
        selected = bpy.context.selected_objects
        # variable
        mat_name_list=[]
        obj_name_list=[]
        ignore_list=[]
        null_mat_obj_list=[]
        empty_cout=0
        changed_count=0
        # Is Only Object
        if is_only_obj:
            # Body
            for obj in selected:
                if obj.active_material.users == 1:
                    obj.name = obj.active_material.name
                    changed_count+=1
                else:
                    ignore_list.append(obj.name)
            # Report
            if len(ignore_list) > 0:
                self.Log(f"{changed_count} Changed!,\tIgnored:{ignore_list}")
                bpy.ops.object.select_all(action='DESELECT')
                # Select Ignored
                for name in ignore_list:
                    bpy.data.objects[name].select_set(True)
            else:
                self.Log(f"Done!")
            # Do Set Mesh Name
            if set_mesh_name:
                bpy.ops.object.f_set_mesh_name()
            return {'FINISHED'}

        # 1.get selected objects active material name by traversal
        for obj in selected:
            # 1.if obj not mesh
            if obj.type != "MESH":
                empty_cout+=1
                continue
            if obj.active_material == None:
                null_mat_obj_list.append(obj.name)
                continue
            mat_name_list.append(obj.active_material.name)
        # 2.convert to set
        mat_name_set = set(mat_name_list)

        #debug
        # P(94, f">> material set: <<")
        # P(93, f"(mat):{mat_name_set}")

        # 3.get object list
        for mat_name in mat_name_set:
            # 4.find obj in scene
            for obj in bpy.data.objects:
                # 5.if have same material
                P(94, f"{obj.name}")
                if obj.type != "MESH" or obj.active_material == None:
                    continue
                if obj.active_material.name == mat_name:
                    # 6.store in list
                    obj_name_list.append(obj.name)
                    # print(f"\033[32m >> {obj.name} << \033[0m")
        # debug
        # P(94, f">> object list: <<")
        # P(94, f"(object):{obj_name_list}")

        # 8.rename object
        removed_obj_name=[]
        # mat
        for mat_name in mat_name_set:
            name_count=suffix_start # start with each mat
            # obj
            for obj_name in obj_name_list:
                # if slots[0] == mat_name : rename and store objects
                if mat_name == bpy.data.objects[obj_name].material_slots[0].name:
                    if obj_name in bpy.context.view_layer:
                        bpy.data.objects[obj_name].select_set(True)
                    removed_obj_name.append(obj_name)
                    # obj name is same as changed name
                    if bpy.data.objects[obj_name].name == f"{mat_name}.{name_count:>0{suffix_number}}":
                        name_count+=1
                        empty_cout+=1
                        continue
                    else:
                        bpy.data.objects[obj_name].name = f"{mat_name}.{name_count:>0{suffix_number}}"
                        name_count+=1
                        changed_count+=1
                        # debug
                        # P(33, f">> {mat_name}:{obj_name} <<")
                        # P(32, f"suffix count:{name_count}")
            # from origin list remove renamed object list
            obj_name_list = list(set(obj_name_list) - set(removed_obj_name))
        if set_mesh_name:
            bpy.ops.object.f_set_mesh_name()
        # 9.report info
        if changed_count == 0 and empty_cout == 0:
            self.Warning(f"Nothing changed")
        else:
            self.Log(f"{changed_count} object renamed, {empty_cout} objects ignored")

        if len(null_mat_obj_list) > 0:
            bpy.ops.object.select_all(action='DESELECT')
            for name in null_mat_obj_list:
                bpy.data.objects[name].select_set(True)
            self.Warning(f"{len(null_mat_obj_list)} objects have no material")
            ...
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
        C = bpy.context
        D = bpy.data
        
        prefix= context.scene.F_EditMaterialNameInSelectedObjects_namePrefix
        ignore=0

        p = re.compile(f"{prefix}")

        mat_set = set(C.object.material_slots.keys())
        for mat in mat_set:
            if p.match(f"{mat}"):
                ignore +=1
                continue
            else:
                D.materials[mat].name = f"{prefix}{D.materials[mat].name}"

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