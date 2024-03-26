from typing import Set
import bpy
import re
from bpy.types import Context

# scene property
bpy.types.Scene.FastOpsObjectSelectBy = bpy.props.EnumProperty(
    name="Object Select By",
    items=[
        ('prefix', 'Prefix', 'By Prefix', 0),
        ('suffix', 'Suffix', 'By Suffix', 1),
        ('both', 'Both', 'By Both', 2),
    ],
    default='prefix'
)

class F_OT_SelectObjectByName(bpy.types.Operator):
    """Select Same Prefix Objects"""
    bl_idname = "object.fastops_select_same_prefix_objects"
    bl_label = "Select Same Prefix Objects"
    bl_options = {'REGISTER', 'UNDO'}
    # select method
    def select_by_name(self, context: Context, type: str):
        # global value
        name_regular_compile = re.compile(r'(?P<prefix>[A-Za-z_]+)(?P<index>\d+)(?P<suffix>_[\w.]+)')
        objects = context.selected_objects
        count=0
        select_list=[]
        # make sure is objects
        if not objects:
            self.report({'ERROR'}, "No Objects Selected")
            return {'CANCELLED'}
        # make sure is right value
        if type not in {'prefix', 'suffix', 'both'}:
            self.report({'ERROR'}, "Invalid Type")
            return {'CANCELLED'}
        # 1.is 'prefix' or 'suffix'
        if not type  == 'both':
            # 2.traversal in selected objects
            for obj in objects:
                # 3.get name part
                name_tmp = name_regular_compile.search(obj.name)
                # make sure name is right
                if not name_tmp:
                    self.report({'ERROR'}, "Illegal Object Name Format")
                    return {'CANCELLED'}                # 3.select object by name part
                target_part = name_tmp.group(type)
                # 4.traversal in data to find...
                for obj in bpy.data.objects:
                    # 5.if have same prefix or suffix
                    if target_part in obj.name:
                        # obj.select_set(True)
                        select_list.append(obj)
                    ...
        # 6.is 'both'
        else:
            # 7.traversal in selected objects
            for obj in objects:
                # get name part
                name_tmp = name_regular_compile.search(obj.name)
                # make sure name is right
                if not name_tmp:
                    self.report({'ERROR'}, "Illegal Object Name Format")
                    return {'CANCELLED'}                # 3.select object by name part
                target_prefix = name_tmp.group('prefix')
                target_suffix = name_tmp.group('suffix')
                self.report({'INFO'}, f"{target_prefix} {target_suffix}")
                # 8.traversal in data to find...
                for obj in bpy.data.objects:
                    # 9.if have same prefix and suffix
                    if target_suffix in obj.name and target_prefix in obj.name:
                        # obj.select_set(True)
                        select_list.append(obj)
                    ...
        return set(select_list)
    def execute(self, context):
        # select method
        select_by = context.scene.FastOpsObjectSelectBy
        obj_list = self.select_by_name(context, select_by)
        if obj_list == {'CANCELLED'}:
            return {'CANCELLED'}
        # select!!!
        self.report({'INFO'}, f"{obj_list}")
        for obj in obj_list:
            obj.select_set(True)
        self.report({'INFO'}, f"selected {len(obj_list)} objects")
        return {'FINISHED'}
    
class F_OT_SelectObjectByMaterial(bpy.types.Operator):
    """Select Object By Material"""
    bl_idname = 'object.fastops_select_object_by_material'
    bl_label = "Select Object By Material"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: bpy.props.StringProperty(name= "Material Name", default="")# type:ignore
    
    def execute(self, context: Context ):
        obj_data = bpy.data.objects
        count=0

        bpy.ops.object.select_all(action='DESELECT')
        for obj in obj_data:
            mat_index = obj.material_slots.find(self.material_name)
            if mat_index == -1:
                continue
            else:
                obj.select_set(True)
                count+=1
                ...
        if count >0:
            self.report({'INFO'}, f"{count} Selected")
        else:
            self.report({'WARNING'}, f"No Object Selected")
        return {'FINISHED'}

    def invoke(self, context, event):

        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    def draw(self, context):
        layout = self.layout

        layout.prop_search(self, "material_name", bpy.data, "materials")
        ...

_cls=[
    F_OT_SelectObjectByName,
    F_OT_SelectObjectByMaterial,
]