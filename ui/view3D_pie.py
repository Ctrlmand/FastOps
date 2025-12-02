import bpy
from ..operators import export, material, material_node, mesh, modifier, object_rename, object_select

class VIEW3D_MT_ModifierPieMenu(bpy.types.Menu):
    """Object Option Pie Menu"""
    bl_idname = "VIEW3D_MT_ModifierPieMenu"
    bl_label = "F Modifier"
    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout

        pie = layout.menu_pie()
        ## Left
        pie.operator(modifier.F_OT_AddModifier.bl_idname, text="Bevel", icon="MOD_BEVEL").modifier_type = 'BEVEL'

        ## Right
        pie.operator(modifier.F_OT_AddModifier.bl_idname, text="Weighted Normal", icon="MOD_NORMALEDIT").modifier_type = 'WEIGHTED_NORMAL'

        ## Down
        col = pie.split().box().column()
        col.label(text="Modifier")
        col.operator(modifier.F_OT_AddModifier.bl_idname, text="Add Modifier", icon="ADD").use_manual_input = True
        col.operator(modifier.F_OT_RemoveModifier.bl_idname, text="Remove Modifier", icon="REMOVE")
        col.operator(object_select.F_OT_SelectByModifier.bl_idname, text="Select By Modifier", icon="RESTRICT_SELECT_OFF")
        col.operator(modifier.F_OT_ClearAllModifier.bl_idname, text="Clear Modifier", icon="TRASH")

        ## Up
        pie.operator(modifier.F_OT_AddModifier.bl_idname, text="Solidify", icon="MOD_SOLIDIFY").modifier_type = 'SOLIDIFY'

        ## Left Up
        pie.operator(modifier.F_OT_AddModifier.bl_idname, text="Array", icon="MOD_ARRAY").modifier_type = 'ARRAY'

        ## Right Up
        pie.operator(modifier.F_OT_AddModifier.bl_idname, text="Mirror", icon="MOD_MIRROR").modifier_type = 'MIRROR'

        ## Left Down
        pie.operator(modifier.F_OT_AddModifier.bl_idname, text="Weld", icon="AUTOMERGE_OFF").modifier_type = 'WELD'

        ## Right Down
        pie.operator(modifier.F_OT_AddModifier.bl_idname, text="Shrinkwrap", icon="MOD_SHRINKWRAP").modifier_type = 'SHRINKWRAP'

class VIEW3D_MT_AlternatePieMenu(bpy.types.Menu):
    """Material Pie Menu"""
    bl_idname = "VIEW3D_MT_MaterialPieMenu"
    bl_label = "F Material"
    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout

        pie = layout.menu_pie()
        ## Left
        pie.operator(material.F_OT_SetDefaultMaterial.bl_idname, text="Flood Empty Material", icon="SHADING_RENDERED")
        
        ## Right
        pie.operator(export.F_OT_ExportFBX.bl_idname, text="Quick Export", icon="EXPORT")

        ## Down
        col = pie.split().box().column()
        col.label(text="UV")
        col.operator(mesh.F_OT_BatchAddUVLayer.bl_idname, text="Add UV Layer", icon="GROUP_UVS")
        col.operator(mesh.F_OT_UnifyUVName.bl_idname, text="Unify UV Name", icon="UV_SYNC_SELECT")
        col.operator(mesh.F_OT_ClearTargetUVMap.bl_idname, text="Clear Target UVLayer", icon="UV")
        col.operator(mesh.F_OT_SwitchUV.bl_idname, text="Switch UVLayer", icon="MOD_UVPROJECT")

        col.split()
        col.label(text="Rename")
        col.operator(object_rename.F_OT_RenameByActiveMaterialName.bl_idname, text="Rename By Active Material Name", icon="OUTLINER_OB_MESH")

        col.split()
        col.label(text="Attribute")
        col.operator(mesh.F_OT_ClearTargetAttribute.bl_idname, text="Clear Target Attribute", icon="TRASH")

        ## Up
        pie.operator(object_select.F_OT_SelectObjectByMaterial.bl_idname, text="Select By Material", icon="MATERIAL_DATA")

        ## Left Up
        pie.operator(material_node.F_OT_FindMaterialByTextureNode.bl_idname, text="Select By Image", icon="OUTLINER_OB_IMAGE")

        ## Right Up
        pie.operator(object_select.F_OT_SelectObjectByName.bl_idname, text="Select By Name", icon="COLLAPSEMENU")

        ## Left Down
        pie.operator(mesh.F_OT_GetMeshMatchedObjects.bl_idname, text="Match Mesh By Name", icon="MESH_DATA")

        ## Right Down
        pie.operator(mesh.F_OT_SetMeshName.bl_idname, text="Set Mesh Name", icon="MESH_DATA")
        

_cls=[
    VIEW3D_MT_ModifierPieMenu,
    VIEW3D_MT_AlternatePieMenu,
]