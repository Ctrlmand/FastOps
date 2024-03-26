import bpy
from ..operators import object_material

# Set Pass Panel
class FASTOPS_PT_SetPassIdSideBar(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "view_layer"
    bl_label = "FastOps"
    def draw(self, context):
        layout = self.layout
        #set pass id
        box = layout.box()
        box.label(text="Set Pass Index")
        row = box.row()
        row.operator(object_material.F_OT_SetAllObjMatID.bl_idname, text="Set Pass ID")

_cls=[
    FASTOPS_PT_SetPassIdSideBar,
]