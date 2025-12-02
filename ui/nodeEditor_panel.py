import bpy
from bpy.types import Panel
from ..operators import material_node
from ..function.utils import get_ntree

class NodePanel:
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "FastOps"
    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return context.space_data.type == 'NODE_EDITOR' and get_ntree() is not None
    
# Set Color Space Panel
class FASTOPS_UI_PT_Node_SetColorSpace(NodePanel, Panel):
    bl_label = "Set Color Space"
    def draw(self, context):
        if context.area.ui_type != "ShaderNodeTree":
            return
        layout = self.layout
        #Texture 
        box = layout.box()
        box.label(text="Tex")
        row = box.row(align=True)
        row.operator(material_node.F_OT_SwitchColorSpace.bl_idname, text="ACES 2.0 sRGB").colorspace = "ACES 2.0 sRGB"
        row.operator(material_node.F_OT_SwitchColorSpace.bl_idname, text="Non-Color").colorspace = "Non-Color"
               
# Merge Tex Panel
class FASTOPS_UI_PT_NodeOptionPanel(NodePanel, Panel):
    bl_label = "Node Options"
    def draw(self, context):
        settings = context.scene.na_settings  # type: ignore
        
        layout = self.layout
        # namual
        box = layout.box()
        box.label(text="Merge RGB And Alpha")
        row = box.row()
        row.operator(material_node.F_OT_ReportSelectedTextureNodeName.bl_idname, text="Texture Name")
        row = box.row()
        row.operator(material_node.F_OT_ImageNodeMergeRGBAndAlpha.bl_idname, text="Merge RGB And Alpha")
        ...

_cls=[
    FASTOPS_UI_PT_Node_SetColorSpace,
    FASTOPS_UI_PT_NodeOptionPanel,
] 