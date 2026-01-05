import bpy
from ..function.classes import Operator
from ..function.export import *
from ..function.debug import *

class F_OT_ExportFBX(Operator):
    """Export FBX"""
    bl_idname = "scene.f_export_fbx"
    bl_label = "Export FBX"
    bl_options = {'REGISTER', 'UNDO'}
    
    batch_mode: bpy.props.EnumProperty(
        name = "Batch Export Mode",
        description = "Way To Batch Export",
        default = 'COLLECTION',
        items =(
            # ('Value', 'Description', 'Tooltip')
            ('OFF', 'Off', 'Set Red Channel'),
            ('SCENE', 'Scene', 'Set Green Channel'),
            ('COLLECTION', 'Collection', 'Set Blue Channel'),
            ('SCENE_COLLECTION', 'SCENE COLLECTION', 'Set Alpha Channel'),
            ('ACTIVE_SCENE_COLLECTION', 'Active Scene Collection', 'Set Color Channel'),
            
        )
    ) # type: ignore

    directory : bpy.props.StringProperty(subtype='DIR_PATH') #type: ignore
    def execute(self, context):
        # folderPath = bpy.path.abspath("//Export")
        folderPath = self.directory
        
        if self.CurrentFileName():
            FileExport.ExportFBX(self, folder_path=folderPath, file_name=self.CurrentFileName(), batch_mode=self.batch_mode)
        return {'FINISHED'}
        ...

    def invoke(self, context, event):
        wm = context.window_manager
        # wm.invoke_props_dialog(self)
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        
        col=layout.column()
        row = col.row()
        row.prop(self, "batch_mode", text="Batch Mode")
        ...

_cls=[
    F_OT_ExportFBX,

]