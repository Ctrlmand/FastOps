import bpy
from ..operators import mesh
class FASTOPS_UI_PT_UVMap(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FastOps"
    bl_label = "UV Maps"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()

        row.prop(context.scene, "F_MeshBatchAddUVLayer_name", text="Name")
        row = box.row()
        row.operator(mesh.F_OT_BatchAddUVLayer.bl_idname, text="Add")
        ...
_cls=[
    FASTOPS_UI_PT_UVMap,
]