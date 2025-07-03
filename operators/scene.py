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
    
    def execute(self, context):
        folder = "E:\\sjw16\\Desktop\\Folder"

        if self.CurrentFileName():
            FileExport.ExportFBX(self, folder_path = folder, file_name= self.CurrentFileName())
        
        return{'FINISHED'}
        ...


_cls=[
    F_OT_ClearScene,
    F_OT_ExportFBX,

]