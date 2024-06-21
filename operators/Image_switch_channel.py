from typing import Any
import bpy
from bpy.types import Context

class F_OT_ImageChannelSet(bpy.types.Operator):
    """Switch Image Display Channel"""
    bl_idname = "image.f_channel_set"
    bl_label = "Set Channel"
    bl_options = {'REGISTER', 'UNDO'}
    
    # blender enum
    channel: bpy.props.EnumProperty(
        name = "Image Channel",
        description = "Image Channel",
        default = 'RED',
        items =(
            # ('Value', 'Description', 'Tooltip')
            ('RED', 'Red', 'Set Red Channel'),
            ('GREEN', 'Green', 'Set Green Channel'),
            ('BLUE', 'Blue', 'Set Blue Channel'),
            ('ALPHA', 'Alpha', 'Set Alpha Channel'),
            ('COLOR', 'Color', 'Set Color Channel'),
            ('COLOR_ALPHA', 'Color Alpha', 'Set Color Alpha Channel')
    )
    ) # type: ignore
    
    def execute(self, context: Context):
        bpy.context.space_data.display_channels = self.channel
        return {'FINISHED'}


_cls=[
    F_OT_ImageChannelSet,
]