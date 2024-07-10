from typing import Any
import bpy
from bpy.types import Context
from ..operators import node_mat, node_mat, window_switch_ui_type

# Set Color Space Panel
class FASTOPS_UI_PT_Node_SetColorSpace(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "FastOps"
    bl_label = "Set Color Space"
    def draw(self, context):
        layout = self.layout
        #Texture 
        box = layout.box()
        box.label(text="Tex")
        row = box.row(align=True)
        row.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="sRBG").colorspace = "Utility - sRGB - Texture"
        row.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="Raw").colorspace = "Utility - Raw"
        
        row = box.row()
        row.operator(node_mat.F_OT_SetColorTexBySuffix.bl_idname, text="Set By Suffix")
        
        #Display
        box = layout.box()
        box.label(text="Display")
        row = box.row(align=True)
        row.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="Rec709").colorspace = 'Utility - Rec.709 - Display'
        row.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="Rec2020").colorspace = 'Utility - Rec.2020 - Display'
# Merge Tex Panel
class FASTOPS_UI_PT_NodeOptionPanel(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "FastOps"
    bl_label = "Node Optiond"
    def draw(self, context):
        layout = self.layout
        
        # namual
        box = layout.box()
        box.label(text="Merge RGB And Alpha")
        row = box.row()
        row.operator(node_mat.F_OT_ReportSelectedTextureNodeName.bl_idname, text="Texture Name")
        row = box.row()
        row.operator(node_mat.F_OT_ImageNodeMergeRGBAndAlpha.bl_idname, text="Merge RGB And Alpha")
        ...

_cls=[
    FASTOPS_UI_PT_Node_SetColorSpace,
    FASTOPS_UI_PT_NodeOptionPanel,
] 