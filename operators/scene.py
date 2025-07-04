import bpy
from ..utility.base_class import Operator
from ..utility.scene import FileExport
from bpy.types import Context

class F_OT_ClearScene(Operator):
    """Clear scene"""
    bl_idname = "object.f_clear_scene"
    bl_label = "Clear Scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context):
        bpy.ops.object.hide_view_clear()
        for var in bpy.context.view_layer.objects:
            var.select_set(True)
        bpy.ops.object.delete(use_global=False)
        bpy.ops.outliner.orphans_purge()
        return{'FINISHED'}

class F_OT_ExportFBX(Operator):
    """Export FBX"""
    bl_idname = "scene.f_export_fbx"
    bl_label = "Export FBX"
    bl_options = {'REGISTER', 'UNDO'}
    
    batch_export: bpy.props.EnumProperty(
        name = "Batch Export Mode",
        description = "Way To Batch Export",
        default = 'OFF',
        items =(
            # ('Value', 'Description', 'Tooltip')
            ('OFF', 'Off', 'Set Red Channel'),
            ('SCENE', 'Scene', 'Set Green Channel'),
            ('COLLECTION', 'Collection', 'Set Blue Channel'),
            ('SCENE_COLLECTION', 'SCENE COLLECTION', 'Set Alpha Channel'),
            ('ACTIVE_SCENE_COLLECTION', 'Active Scene Collection', 'Set Color Channel'),
            
        )
    ) # type: ignore
# 'OFF', 'SCENE', 'COLLECTION', 'SCENE_COLLECTION', 'ACTIVE_SCENE_COLLECTION'
    def execute(self, context):
        folder = "C:\\BlenderExport"

        if self.CurrentFileName():
            FileExport.ExportFBX(self, folder_path = folder, file_name= self.CurrentFileName(), batch_mode=self.batch_export)
        
        return{'FINISHED'}
        ...

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        
        col=layout.column()
        row = col.row()
        row.prop(self, "batch_export", text="Batch Mode")
        ...

_cls=[
    F_OT_ClearScene,
    F_OT_ExportFBX,

]