import bpy
from ..operators import obj_move_to_collection_by_name

# Move To Collection By Name Panel
class VIEW3D_PT_MoveToCollectionByName(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FastOps" 
    bl_label = "Move To Collection"
    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Group By Name")
        row = box.row()
        row.operator(obj_move_to_collection_by_name.F_OT_ObjMoveToCollectionByName.bl_idname, text="Group it!")

_cls=[
    VIEW3D_PT_MoveToCollectionByName,
]