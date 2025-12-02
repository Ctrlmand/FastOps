import bpy
from ..operators import material_node

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
        row.operator(material_node.F_OT_SwitchColorSpace.bl_idname, text="ACES 2.0 sRGB").colorspace = "ACES 2.0 sRGB"
        row.operator(material_node.F_OT_SwitchColorSpace.bl_idname, text="Non-Color").colorspace = "Non-Color"
               
# Merge Tex Panel
class FASTOPS_UI_PT_NodeOptionPanel(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "FastOps"
    bl_label = "Node Options"
    def draw(self, context):
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