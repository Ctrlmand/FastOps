# from typing import Any
# import bpy
# from bpy.types import Context


# class F_OT_SelectObjectByMaterial(bpy.types.Operator):
#     """Select Object By Material"""
#     bl_idname = 'object.fastops_select_object_by_material'
#     bl_label = "Select Object By Material"
#     bl_options = {'REGISTER', 'UNDO'}

#     material_name: bpy.props.StringProperty(name= "Material Name", default="")# type:ignore
    
#     def execute(self, context: Context | Any) -> Context | Any:
#         obj_data = bpy.data.objects

#         bpy.ops.object.select_all(action='DESELECT')

#         for obj in obj_data:
#             mat_index = obj.material_slots.find(self.material_name)
#             if mat_index == -1:
#                 continue
#             else:
#                 obj.select_set(True)
#                 ...
#         return {'FINISHED'}
    
#     def invoke(self, context, event):

#         wm = context.window_manager
#         return wm.invoke_props_dialog(self)
#     def draw(self, context):
#         layout = self.layout

#         layout.prop_search(self, "material_name", bpy.data, "materials")
#         ...
    
# bpy.utils.register_class(F_OT_SelectObjectByMaterial)

# bpy.ops.object.fastops_select_object_by_material()