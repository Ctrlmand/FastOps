from typing import Any, Set
import bpy
from bpy.types import Context

class F_OT_SwitchColorSpace(bpy.types.Operator):
    """Switch Textures Color Space"""
    bl_idname = "node.fastops_switch_color_space"
    bl_label = "Switch Color Space"
    bl_options = {'REGISTER', 'UNDO'}

    # enum
    colorspace: bpy.props.EnumProperty(
        name = "Image Color Space",
        description = "Image Color Space",
        default = 'Utility - Raw',
        items =(
            ('Utility - Raw', 'Raw', 'Set Space As Raw'),
            ('Utility - sRGB - Texture', 'sRGB', 'Set Space As sRGB'),
            ('Utility - Rec.709 - Display', 'Rec.709', 'Set Space As Rec.709'),
            ('Utility - Rec.2020 - Display', 'Rec.2020', 'Set Space As Rec.2020'),
        )
    ) # type: ignore

    def execute(self, context: Context):
        sucess_count=0
        fail_count=0
        for node in context.selected_nodes:
            # self.report({'INFO'}, f"{node.image}")
            if node.type == "TEX_IMAGE":
                node.image.colorspace_settings.name = self.colorspace
                sucess_count+=1
                ...
            else:
                fail_count+=1
        if sucess_count>0:
            self.report({'INFO'},f"{sucess_count} nodes sucessfully changed, {fail_count} nodes failed")
        else:
            self.report({'WARNING'},f"no texture nodes found")
        return {'FINISHED'}

class F_OT_SetColorTexBySuffix(bpy.types.Operator):
    """Set Color Space By Suffix"""
    bl_idname = "node.fastops_set_color_tex_by_suffix"
    bl_label = "Set Color Space By Suffix"
    bl_options = {'REGISTER', "UNDO"}
    def execute(self, context: Context):
        suffixes_to_check = ['_BaseColor', '_Albedo', '_Color', '_Emissive', '_Emiss']
        for img in bpy.data.images:
            # is color tex
            if any(suffix in img.name for suffix in suffixes_to_check):
                img.colorspace_settings.name = 'Utility - sRGB - Texture'
                # report img name that was changed
                # self.report({'INFO'}, f"{img.name}")
            else:
                img.colorspace_settings.name = 'Utility - Raw'
        return {'FINISHED'}

_cls=[
    F_OT_SwitchColorSpace,
    F_OT_SetColorTexBySuffix,
]