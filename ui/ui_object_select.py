import bpy
from bpy.types import Context
from ..operators import object_select

# Select Object Panel
class FASTOPS_PT_SelectObject(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FastOps"
    bl_label = "Select"
    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Select by name")
        row = box.row()
        row.prop(context.scene, "FastOpsObjectSelectBy", text="Select By")
        row = box.row()
        row.operator(object_select.F_OT_SelectObjectByName.bl_idname, text="Select!")

_cls=[
    FASTOPS_PT_SelectObject,
]