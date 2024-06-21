import bpy

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