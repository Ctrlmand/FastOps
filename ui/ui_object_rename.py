import bpy
from ..operators import object_rename, obj_move_to_collection_by_name

# Rename Panel 
class FASTOPS_PT_RenameSideBar(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FastOps"
    bl_label = "Rename"

    def draw(self, context):
        layout = self.layout

        # label
        box = layout.box()
        box.label(text="Object")
        
        # get name
        row = box.row()
        row.prop(context.scene, "F_ObjectBatchRename_namePrefix", text="Name")

        # get suffix
        row = box.row()
        row.prop(context.scene, "F_ObjectBatchRename_addSuffix", text = "Suffix")

        # get mount
        row = box.row(align= True)
        row.prop(context.scene, "F_ObjectBatchRename_suffixStart", text="Start")
        row.prop(context.scene, "F_ObjectBatchRename_suffixNumber", text="Digit")

        # is/not only suffix
        row = box.row()
        row.prop(context.scene, "F_ObjectBatchRename_isOnlyAddSuffix", text= "Only Suffix")

        # call operator
        row = box.row()
        row.operator(object_rename.F_OT_ObjectBatchRename.bl_idname, text="Rename")

        # find and replace
        box.split()
        box.label(text="Find And Replace")
        row = box.row()
        row.prop(context.scene, "FastOpsObjectBatchRename_find", text="Find")
        row = box.row()
        row.prop(context.scene, "FastOpsObjectBatchRename_replace", text="Replace")
        row = box.row()
        row.operator(object_rename.F_OT_FindAndReplace.bl_idname, text="Find And Replace")

        # rename material
        box.label(text="Material")
        row = box.row()
        row.prop(context.scene, 'F_EditMaterialNameInSelectedObjects_namePrefix', text="Prefix")
        row = box.row()
        row.operator(object_rename.F_OT_EditMaterialNameInSelectedObjects.bl_idname, text="Edit Material Name")

        # group by name
        layout = self.layout
        row= layout.row()

        row.label(text="Group By Name")
        row = layout.row()
        row.operator(obj_move_to_collection_by_name.F_OT_ObjMoveToCollectionByName.bl_idname, text="Group it!")
_cls=[
    FASTOPS_PT_RenameSideBar,
]