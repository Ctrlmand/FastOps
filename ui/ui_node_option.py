from typing import Any
import bpy
from bpy.types import Context
from ..operators import node_merge_tex_channel, node_change_colorspace, window_switch_ui_type

# Set Color Space Panel
class FASTOPS_PT_Node_SetColorSpacePanel(bpy.types.Panel):
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
        row.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="sRBG").colorspace = "Utility - sRGB - Texture"
        row.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="Raw").colorspace = "Utility - Raw"
        
        row = box.row()
        row.operator(node_change_colorspace.F_OT_SetColorTexBySuffix.bl_idname, text="Set By Suffix")
        
        #Display
        box = layout.box()
        box.label(text="Display")
        row = box.row(align=True)
        row.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="Rec709").colorspace = 'Utility - Rec.709 - Display'
        row.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="Rec2020").colorspace = 'Utility - Rec.2020 - Display'
# Merge Tex Panel
class FASTOPS_PT_NodeOptionPanel(bpy.types.Panel):
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
        row.operator(node_merge_tex_channel.F_OT_ReportSelectedTextureNodeName.bl_idname, text="Texture Name")
        row = box.row()
        row.operator(node_merge_tex_channel.F_OT_ImageNodeMergeRGBAndAlpha.bl_idname, text="Merge RGB And Alpha")
        ...

# Node Option Pie Menu
class FASTOPS_MT_NodeOptionPieMenu(bpy.types.Menu):
    """Node Option Pie Menu"""
    bl_idname = "FASTOPS_MT_NodeOptionPieMenu"
    bl_label = "Node Option"
    def draw(self, context: Context):
        # In Shader Editor
        if bpy.context.area.ui_type == 'ShaderNodeTree':
            layout = self.layout
            pie = layout.menu_pie()

            ## Left
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="<-") 

            ## Right
            col = pie.split().box().column()

            col.label(text="Merge RGB And Alpha")
            col.operator(node_merge_tex_channel.F_OT_ReportSelectedTextureNodeName.bl_idname, text="Repoet Texture Name")
            col.operator(node_merge_tex_channel.F_OT_ImageNodeMergeRGBAndAlpha.bl_idname, text="Merge It")

            ## Down
            col = pie.split().box().column()
            col.label(text="Set Color Space")
            row = col.row(align=True)
            row.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="Color").colorspace = 'Utility - sRGB - Texture'
            row.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="Raw").colorspace = 'Utility - Raw'
            col.operator(node_change_colorspace.F_OT_SetColorTexBySuffix.bl_idname, text="Set By Suffix")
            col.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="Rec709").colorspace = 'Utility - Rec.709 - Display'
            col.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="Rec2020").colorspace = 'Utility - Rec.2020 - Display'

            ## Up
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="Geometry Node Tree", icon="NODETREE").ui_type = "GeometryNodeTree"

            ## Left Up
            pie.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="\\")

            ## Right Up
            pie.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="/")

            ## Left Down
            pie.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="/")

            ## Right Down
            pie.operator(node_change_colorspace.F_OT_SwitchColorSpace.bl_idname, text="\\")
                        
        if bpy.context.area.ui_type == 'GeometryNodeTree':
            layout = self.layout
            pie = layout.menu_pie()

            ## Left
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="<-", icon="NODETREE")

            ## Right
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="->", icon="NODETREE")
            
            ## Down
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="|", icon="NODETREE")

            ## Up
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="Shader Editor", icon="NODE_MATERIAL").ui_type = "ShaderNodeTree"

            ## Left Up
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="\\", icon="NODETREE")

            ## Right Up
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="/", icon="NODETREE")

            ## Left Down
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="/", icon="NODETREE")

            ## Right Down
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="\\", icon="NODETREE")
            ...
        if bpy.context.area.ui_type == 'CompositorNodeTree':
            layout = self.layout
            pie = layout.menu_pie()

            ## Left
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="<-", icon="NODETREE")

            ## Right
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="->", icon="NODETREE")
            
            ## Down
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="|", icon="NODETREE")

            ## Up
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="Shader Editor", icon="NODE_MATERIAL").ui_type = "ShaderNodeTree"

            ## Left Up
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="\\", icon="NODETREE")

            ## Right Up
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="/", icon="NODETREE")

            ## Left Down
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="/", icon="NODETREE")

            ## Right Down
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="\\", icon="NODETREE")
            
            ...
_cls=[
    FASTOPS_PT_Node_SetColorSpacePanel,
    FASTOPS_PT_NodeOptionPanel,
    FASTOPS_MT_NodeOptionPieMenu,
] 