import bpy
from bpy.types import Context


class F_OT_Check_Ui_Type(bpy.types.Operator):
    """Check UI Type"""
    bl_idname = "area.fastops_check_ui_type"
    bl_label = "Check UI Type"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context) :
        self.report({'INFO'}, f"{bpy.context.area.ui_type}")
        return {'FINISHED'}

class F_OT_SwitchUiType(bpy.types.Operator):
    """Switch UI Type"""
    bl_idname = "window.fastops_switch_ui_type"
    bl_label = "Switch UI Type"
    bl_options = {'REGISTER', 'UNDO'}

    # enum
    ui_type: bpy.props.EnumProperty(
        name = "Window UI Type",
        description = "Change Window UI Type",
        default = 'GeometryNodeTree',
        items =(
            ('GeometryNodeTree', 'Geometry Node Tree', 'Geometry Node Tree'),
            ('ShaderNodeTree', 'Shader Node Tree', 'Shader Node Tree'),
            ('TextureNodeTree', 'Texture Node Tree', 'Texture Node Tree'),
        )
    )# type: ignore

    def execute(self, context: bpy.types.Context):
        context.area.ui_type = self.ui_type

        self.report({'INFO'}, f"Switch UI Type To {self.ui_type}")
        return {'FINISHED'}
_cls=[
    F_OT_SwitchUiType,
    F_OT_Check_Ui_Type,
]