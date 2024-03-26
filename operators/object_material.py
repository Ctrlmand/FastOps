from typing import Any
import bpy
from bpy.types import Context

class F_OT_SetAllObjMatID(bpy.types.Operator):
    """Set all object's and material's pass id"""
    bl_idname = "object.fastops_set_all_obj_mat_pass_id"
    bl_label = "Set All Object Material Pass ID"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):
        #set object's pass id
        i=0
        for index, obj in enumerate(bpy.data.objects):
            obj.pass_index = index
            obj_count=index
        #set material pass id
        for index, mat in enumerate(bpy.data.materials):
            mat.pass_index = index
            mat_count=index
        #report seting counting
        self.report({'INFO'},
            f"{obj_count} objects and {mat_count} materials changed")
        ###End of Set All Object Material Pass ID
        return {'FINISHED'}
    
class F_OT_SetNoneMaterial(bpy.types.Operator):
    """Set None Material"""
    bl_idname = "object.fastops_set_none_material"
    bl_label = "Set None Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context | Any) -> Context | Any:
        count=0
        ignore=0

        if 'Material' not in bpy.data.materials:
            bpy.data.materials.new('Material')
            
        for obj in bpy.data.objects:
            if obj.active_material is None and obj.type == 'MESH':
                obj.active_material=bpy.data.materials['Material']
                count+=1
            else:
                ignore+=1
                continue
        self.report({ 'INFO' }, f'Sucessfully:{count}, Ignore:{ignore}')
        return {'FINISHED'}

_cls=[
    F_OT_SetNoneMaterial,
    F_OT_SetAllObjMatID,
]
