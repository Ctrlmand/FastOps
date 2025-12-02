from typing import Any
import bpy
from bpy.types import Context
from ..function.classes import Operator

class F_OT_SetAllObjMatID(Operator):
    """Set all object's and material's pass id"""
    bl_idname = "object.f_set_all_obj_mat_pass_id"
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
        self.Log(f"{obj_count} objects and {mat_count} materials changed")
        ###End of Set All Object Material Pass ID
        return {'FINISHED'}
    
class F_OT_SetDefaultMaterial(Operator):
    """Set Default Material"""
    bl_idname = "object.f_set_default_material"
    bl_label = "Set Default Material"
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
        self.Log(f'Sucessfully:{count}, Ignore:{ignore}')
        return {'FINISHED'}

_cls=[
    F_OT_SetDefaultMaterial,
    F_OT_SetAllObjMatID,
]
