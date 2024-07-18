import bpy
from ..operators import object_modifier, object_material, object_rename, object_select, node_mat

class VIEW3D_MT_ModifierPieMenu(bpy.types.Menu):
    """Object Option Pie Menu"""
    bl_idname = "VIEW3D_MT_ModifierPieMenu"
    bl_label = "F Modifier"
    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout

        pie = layout.menu_pie()
        ## Left
        pie.operator(object_modifier.F_OT_AddModifier.bl_idname, text="Bevel", icon="MOD_BEVEL").modifier_type = 'BEVEL'

        ## Right
        pie.operator(object_modifier.F_OT_AddModifier.bl_idname, text="Weighted Normal", icon="MOD_NORMALEDIT").modifier_type = 'WEIGHTED_NORMAL'

        ## Down
        col = pie.split().box().column()
        col.operator(object_modifier.F_OT_AddModifier.bl_idname, text="Add Modifier", icon="ADD").use_manual = True
        col.operator(object_modifier.F_OT_RemoveModifier.bl_idname, text="Remove Modifier", icon="REMOVE")
        col.operator(object_select.F_OT_SelectByModifier.bl_idname, text="Select By Modifier", icon="RESTRICT_SELECT_OFF")
        col.operator(object_modifier.F_OT_ClearAllModifier.bl_idname, text="Clear Modifier", icon="TRASH")

        ## Up
        pie.operator(object_modifier.F_OT_AddModifier.bl_idname, text="Solidify", icon="MOD_SOLIDIFY").modifier_type = 'SOLIDIFY'

        ## Left Up
        pie.operator(object_modifier.F_OT_AddModifier.bl_idname, text="Array", icon="MOD_ARRAY").modifier_type = 'ARRAY'

        ## Right Up
        pie.operator(object_modifier.F_OT_AddModifier.bl_idname, text="Mirror", icon="MOD_MIRROR").modifier_type = 'MIRROR'

        ## Left Down
        pie.operator(object_modifier.F_OT_AddModifier.bl_idname, text="Weld", icon="AUTOMERGE_OFF").modifier_type = 'WELD'

        ## Right Down
        pie.operator(object_modifier.F_OT_AddModifier.bl_idname, text="Shrinkwrap", icon="MOD_SHRINKWRAP").modifier_type = 'SHRINKWRAP'

class VIEW3D_MT_MaterialPieMenu(bpy.types.Menu):
    """Material Pie Menu"""
    bl_idname = "VIEW3D_MT_MaterialPieMenu"
    bl_label = "F Material"
    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout

        pie = layout.menu_pie()
        ## Left
        pie.operator(object_material.F_OT_SetNoneMaterial.bl_idname, text="Flood Empty Material", icon="SHADING_RENDERED")
        
        ## Right
        pie.operator(object_rename.F_OT_RenameByActiveMaterialName.bl_idname, text="Rename By Active Material Name", icon="OUTLINER_OB_MESH")

        ## Down
        pie.operator(object_rename.F_OT_SetMeshName.bl_idname, text="Set Mesh Name", icon="MESH_DATA")

        ## Up
        pie.operator(object_select.F_OT_SelectObjectByMaterial.bl_idname, text="Select By Material", icon="MATERIAL_DATA")

        ## Left Up
        pie.operator(node_mat.F_OT_FindMaterialByTextureNode.bl_idname, text="Select By Image", icon="OUTLINER_OB_IMAGE")
_cls=[
    VIEW3D_MT_ModifierPieMenu,
    VIEW3D_MT_MaterialPieMenu,
]