import bpy
from ..operators import node_mat, node_mat, window_switch_ui_type

# Node Option Pie Menu
class FASTOPS_MT_NodeOptionPieMenu(bpy.types.Menu):
    """Node Option Pie Menu"""
    bl_idname = "FASTOPS_MT_NodeOptionPieMenu"
    bl_label = "Node Option"
    def draw(self, context):
        # In Shader Editor
        if bpy.context.area.ui_type == 'ShaderNodeTree':
            layout = self.layout
            pie = layout.menu_pie()

            ## Left
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="<-") 

            ## Right
            col = pie.split().box().column()

            col.label(text="Merge RGB And Alpha")
            col.operator(node_mat.F_OT_ReportSelectedTextureNodeName.bl_idname, text="Repoet Texture Name")
            col.operator(node_mat.F_OT_ImageNodeMergeRGBAndAlpha.bl_idname, text="Merge It")

            ## Down
            col = pie.split().box().column()
            col.label(text="Set Color Space")
            row = col.row(align=True)
            row.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="Color").colorspace = 'Utility - sRGB - Texture'
            row.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="Raw").colorspace = 'Utility - Raw'
            col.operator(node_mat.F_OT_SetColorTexBySuffix.bl_idname, text="Set By Suffix")
            col.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="Rec709").colorspace = 'Utility - Rec.709 - Display'
            col.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="Rec2020").colorspace = 'Utility - Rec.2020 - Display'

            ## Up
            pie.operator(window_switch_ui_type.F_OT_SwitchUiType.bl_idname, text="Geometry Node Tree", icon="NODETREE").ui_type = "GeometryNodeTree"

            ## Left Up
            pie.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="\\")

            ## Right Up
            pie.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="/")

            ## Left Down
            pie.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="/")

            ## Right Down
            pie.operator(node_mat.F_OT_SwitchColorSpace.bl_idname, text="\\")
                        
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
    FASTOPS_MT_NodeOptionPieMenu,
]