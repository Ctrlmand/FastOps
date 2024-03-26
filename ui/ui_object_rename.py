import bpy
from ..operators import object_rename

# Rename Panel 
class FASTOPS_PT_RenameSideBar(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FastOps"
    bl_label = "Rename"

    def draw(self, context):
        layout = self.layout

        #label
        box = layout.box()
        box.label(text="Rename Utility")
        #get name
        row = box.row()
        row.prop(context.scene, "FastOpsObjectBatchRename_namePrefix", text="Name")
        #get suffix
        row = box.row()
        row.prop(context.scene, "FastOpsObjectBatchRename_addSuffix", text = "Suffix")
        #get mount
        row = box.row(align= True)
        row.prop(context.scene, "FastOpsObjectBatchRename_suffixStart", text="Start")
        row.prop(context.scene, "FastOpsObjectBatchRename_suffixNumber", text="Digit")
        #is/not only suffix
        row = box.row()
        row.prop(context.scene, "FastOpsObjectBatchRename_isOnlyAddSuffix", text= "Only Suffix")
        #call operator
        row = box.row(align= True)
        row.operator(object_rename.F_OT_ObjectBatchRename.bl_idname, text="Rename")
        row.operator(object_rename.F_OT_SetMeshName.bl_idname, text="SetName")
        #rename by active material name
        row = box.row()
        row.operator(object_rename.F_OT_RenameByActiveMaterialName.bl_idname, text="Use Active Material Name")
        #find and replace
        row = box.row()
        row.prop(context.scene, "FastOpsObjectBatchRename_find", text="Find")
        row = box.row()
        row.prop(context.scene, "FastOpsObjectBatchRename_replace", text="Replace")
        row = box.row()
        row.operator(object_rename.F_OT_FindAndReplace.bl_idname, text="Find And Replace")

_cls=[
    FASTOPS_PT_RenameSideBar,
]