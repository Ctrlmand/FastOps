import bpy
from ..operators import mesh

# Edit Normal Panel
class FASTOPS_UI_PT_EditNormal(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FastOps"
    bl_label = "Edit Normal"

    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Edit split normal")
        row = box.row(align=True)
        row.operator(mesh.F_OT_AddSplitNormal.bl_idname, text="Add")
        row.operator(mesh.F_OT_ClearSplitNormal.bl_idname, text="Clear")

        box.label(text="Edit sharp")
        row = box.row()
        row.operator(mesh.F_OT_ClearSharp.bl_idname, text="Clear Sharp")

_cls=[
    FASTOPS_UI_PT_EditNormal,
]