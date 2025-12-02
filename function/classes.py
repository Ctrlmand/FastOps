import bpy
from pathlib import Path

class Operator(bpy.types.Operator):
    """"Operator Base Class"""
    bl_idname = "object.f_operator_base_class"
    bl_label = "Operator Base Blass"
    bl_options = {'REGISTER', 'UNDO'}
    
    def Log(self, info):
        self.report({'INFO'}, info)
    def Warning(self, info):
        self.report({'WARNING'}, info)
    def Error(self, info):
        self.report({'ERROR'}, info)
    def CurrentFileName(self) -> str:
        if not bpy.data.filepath:
            self.Warning("Save blend file first")
            return None

        path = Path(bpy.data.filepath)
        return path.stem
        