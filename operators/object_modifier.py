from typing import Any
import bpy
import math
from mathutils import Vector
from bpy.types import Context
from ..utility.base_class import Operator
from ..utility.debug import P
from ..utility import props

class F_OT_AddModifier(Operator):
    """Batch Add Modifier To Selected Objects"""
    bl_idname = "object.f_add_modifier"
    bl_label = "Modifier"
    bl_options = {'REGISTER', 'UNDO'}
    # Variables
    # enum property
    modifier_type: props.get_modifier_enum() # type: ignore

    # Bevel
    bevel_affect: bpy.props.EnumProperty( # type: ignore
        name = "Bevel Affect",
        description = "Bevel Affect",
        items = (
            ('VERTICES', 'Vertices', ''),
            ('EDGES', 'Edges', ''),
        ),
        default = 'EDGES'
    )
    bevel_offset_type: bpy.props.EnumProperty( # type: ignore
        name = "Bevel Offset Type",
        description = "Bevel Offset Type",
        items = (
            ('OFFSET', 'Offset', ''),
            ('WIDTH', 'Width', ''),
            ('DEPTH', 'Depth', ''),
            ('PERCENT', 'Percent', ''),
            ('ABSOLUTE', 'Absolute', ''),
        ),
        default = 'OFFSET'
    )

    bevel_width: bpy.props.FloatProperty(name = "Bevel Width", default=0.1, min=0.0, max=100.0) # type: ignore

    bevel_segments: bpy.props.IntProperty(name= "Bevel Segments", min=1) # type: ignore
    bevel_limit_method: bpy.props.EnumProperty(# type: ignore
        name = "Bevel Limit Method",
        description = "Bevel Limit Method",
        items =(
            ('NONE', "None", "None"),
            ('ANGLE', 'Angle', 'Angle'),
            ('WEIGHT', 'Weight', 'Weight'),
            ('VGROUP', 'Vertex Group', 'Vertex Group')
        ),
        default = 'ANGLE',
    ) 
    bevel_angle_limit: bpy.props.FloatProperty(name = "Bevel Limit Angle", step=1, default = math.acos(0.0)/3, min = 0.0, max = math.acos(0.0)*2, subtype = 'ANGLE') # type: ignore
    bevel_profile: bpy.props.FloatProperty(name= "Bevel Profile", default=0.5, min=0, max=1) # type: ignore
    bevel_use_clamp_overlap: bpy.props.BoolProperty(name= "Use Clamp Overlap", default=False) # type: ignore

    # Mirror
    mirror_use_x: bpy.props.BoolProperty(name="Mirror Use X", default=True) # type: ignore
    mirror_use_y: bpy.props.BoolProperty(name="Mirror Use Y", default=False) # type: ignore
    mirror_use_z: bpy.props.BoolProperty(name="Mirror Use Z", default=False) # type: ignore

    mirror_use_clip: bpy.props.BoolProperty(name="Mirror Use Clip", default=True) # type: ignore

    mirror_offset_u: bpy.props.FloatProperty(name="Mirror Offset U", default=1.0, min=0.0, max=1.0) # type: ignore
    mirror_offset_v: bpy.props.FloatProperty(name="Mirror Offset V", default=0.0, min=0.0, max=1.0) # type: ignore

    # Solidify
    solidify_thickness: bpy.props.FloatProperty(name="Solidify Thickness", default=0.01, subtype='DISTANCE') # type: ignore
    solidify_offset: bpy.props.FloatProperty(name="Solidify Offset", default=-1.0, min=-1.0, max=1.0) # type: ignore
    solidify_use_even_offset: bpy.props.BoolProperty(name="Even Offset", default=True) # type: ignore
    solidify_use_rim: bpy.props.BoolProperty(name="Use Rim", default=True) # type: ignore
    solidify_use_rim_only: bpy.props.BoolProperty(name="Use Rim Only", default=False) # type: ignore

    # Shrinkwarp
    shrinkwarp_wrap_method: bpy.props.EnumProperty( # type: ignore
        name = "Wrap Method",
        description = "Shrinkwarp Wrap Method",
        default ="PROJECT",
        items =(
            ('NEAREST_SURFACEPOINT', "Nearest Surface Point", ""),
            ('PROJECT', "Project", ""),
            ('NEAREST_VERTEX', "Nearest Vertex", ""),
            ('TARGET_PROJECT', "Target Project", ""),
        ),
    )
    shrinkwarp_use_negative_direction: bpy.props.BoolProperty(name="Negative Direction", default=True) # type: ignore
    shrinkwarp_offset: bpy.props.FloatProperty(name="Offset", default=0.01, subtype='DISTANCE') # type: ignore

    # Array
    array_relative_offset_displace: bpy.props.FloatVectorProperty(name="Relative Offset Displace", default=(2.0, 0.0, 0.0)) # type: ignore

    array_along_single_axis: bpy.props.BoolProperty(name="Along Single Axis", default=True) # type: ignore
    array_use_object_offset: bpy.props.BoolProperty(name="Use Object Offset", default=False) # type: ignore

    # Triangulate
    triangulate_keep_custom_normals: bpy.props.BoolProperty(name="Keep Custom Normals", default=True) # type: ignore
    triangulate_min_vertices: bpy.props.IntProperty(name="Min Vertices", default=4) # type: ignore

    array_set_axis: bpy.props.EnumProperty( # type: ignore
        name = "Array Set Axis",
        description = "Array Set Axis",
        default = 'X',
        items =(
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
        ),
    )

    # Manual
    use_manual: bpy.props.BoolProperty(name="Use Manual", default=False) # type: ignore
    
    def execute(self, context: bpy.types.Context):
        # alias
        active_object = bpy.context.object
        selected_objects = bpy.context.selected_objects

        # Bevel
        if self.modifier_type == 'BEVEL':
           # interation
           for obj in selected_objects:
                context.view_layer.objects.active = obj
                obj.modifiers.new(name=str.title(self.modifier_type), type = self.modifier_type)

                mod=obj.modifiers[-1]
                
                mod.affect = self.bevel_affect
                mod.width = self.bevel_width
                mod.segments = self.bevel_segments

                mod.limit_method = self.bevel_limit_method
                # if Angle
                if self.bevel_limit_method == 'ANGLE':
                    mod.angle_limit = self.bevel_angle_limit

                mod.profile = self.bevel_profile

                mod.use_clamp_overlap = self.bevel_use_clamp_overlap
        # Mirror
        elif self.modifier_type == 'MIRROR':
            # add modifier
            active_object.modifiers.new(name=str.title(self.modifier_type), type = self.modifier_type)

            mod = context.object.modifiers[-1]
            
            # is tow objects selected? 
            if len(selected_objects) == 2:
                # mirror object
                tmp_list = selected_objects
                tmp_list.remove(active_object)
                mirror_obj = tmp_list[0]
                # debug
                P(31, f"active object:{active_object.name}")
                P(31, f"another object:{mirror_obj.name}")
                # set
                mod.mirror_object = mirror_obj
                
            elif len(selected_objects) > 2 or len(selected_objects) < 1:
                self.Error(f"Please Select 1 or 2 Objects")
                return {'CANCELLED'}
            
            # set modifier
            mod.use_axis[0] = self.mirror_use_x
            mod.use_axis[1] = self.mirror_use_y
            mod.use_axis[2] = self.mirror_use_z

            mod.use_clip = self.mirror_use_clip

            mod.offset_u = self.mirror_offset_u
            mod.offset_v = self.mirror_offset_v


            ...
        # Solidify
        elif self.modifier_type == 'SOLIDIFY':
            active_object.modifiers.new(name=str.title(self.modifier_type), type = self.modifier_type)
            mod = context.object.modifiers[-1]

            mod.thickness = self.solidify_thickness
            mod.offset = self.solidify_offset
            mod.use_even_offset = self.solidify_use_even_offset
            mod.use_rim = self.solidify_use_rim
            mod.use_rim_only = self.solidify_use_rim_only
        # Shrinkwrap
        elif self.modifier_type == 'SHRINKWRAP':
            # add modifier
            active_object.modifiers.new(name=str.title(self.modifier_type), type = self.modifier_type)

            mod = context.object.modifiers[-1]
            
            # is tow objects selected? 
            if len(selected_objects) == 2:
                # target object
                tmp_list = selected_objects
                tmp_list.remove(active_object)
                target_obj = tmp_list[0]
                # set
                mod.target = target_obj
            elif len(selected_objects) > 2:
                self.Error(f"Too Many Objects")
                return {'CANCELLED'}
            elif len(selected_objects) < 2:
                self.Error(f"Too Few Objects")
                return {'CANCELLED'}
            
            # set modifier
            mod.wrap_method = self.shrinkwarp_wrap_method
            mod.use_negative_direction = self.shrinkwarp_use_negative_direction
            mod.offset = self.shrinkwarp_offset
        # Array
        elif self.modifier_type == 'ARRAY':
            active_object.modifiers.new(name=str.title(self.modifier_type), type = self.modifier_type)
            mod = mod = context.object.modifiers[-1]

            # set axis
            if self.array_along_single_axis:
                match self.array_set_axis:
                    case 'X':
                        self.array_relative_offset_displace = (2.0, 0.0, 0.0)
                    case 'Y':
                        self.array_relative_offset_displace = (0.0, 2.0, 0.0)
                    case 'Z':
                        self.array_relative_offset_displace = (0.0, 0.0, 2.0)
                ...

            # use object offset
            if self.array_use_object_offset:
                empty_name = f'{context.object.name}_ObjectOffset'

                if not empty_name in bpy.data.objects:
                    # set mode
                    mod.use_relative_offset = False
                    mod.use_object_offset = True
                    mod.count = 3

                    # create empty
                    bpy.data.objects.new(empty_name, None)
                    context.scene.collection.objects.link(bpy.data.objects[empty_name])
                    bpy.data.objects[empty_name].location = context.object.location + Vector((0, 0, 2))
                    mod.offset_object = bpy.data.objects[empty_name]

                    bpy.ops.object.select_all(action='DESELECT')
                    context.view_layer.objects.active = bpy.data.objects[empty_name]
                    bpy.data.objects[empty_name].select_set(True)

            # set modifier value
            mod.relative_offset_displace[0] = self.array_relative_offset_displace[0]
            mod.relative_offset_displace[1] = self.array_relative_offset_displace[1]
            mod.relative_offset_displace[2] = self.array_relative_offset_displace[2]
        # Triangulate
        elif self.modifier_type == 'TRIANGULATE':
            for obj in selected_objects:
                obj.modifiers.new(name=str.title(self.modifier_type), type = self.modifier_type)
                mod = context.object.modifiers[-1]

                mod.keep_custom_normals = self.triangulate_keep_custom_normals
                mod.min_vertices = self.triangulate_min_vertices
        # Basic
        else:
            for obj in selected_objects:
                obj.modifiers.new(name=str.title(self.modifier_type), type = self.modifier_type)
        
        # set use_manual as false when finished
        if self.use_manual:
            self.use_manual = False
        self.Log(f"{len(selected_objects)} Objects Added <{self.modifier_type}>")
        return {'FINISHED'}

    def draw(self, context: Context):
        layout = self.layout
        col=layout.column()

        # Bevel
        if self.modifier_type == 'BEVEL':
            col.use_property_split = True
            self.use_manual_type(self.use_manual,col)

            row = col.row()
            row.prop(self, 'bevel_affect', expand=True)
            col.prop(self, 'bevel_offset_type', text="Offset Type")
            col.prop(self, 'bevel_width', text="Amount")
            col.prop(self, 'bevel_segments', text="Segments")

            col.split()

            col.prop(self, 'bevel_limit_method', text="Limit Method")
            if self.bevel_limit_method == 'ANGLE':
                col.prop(self, 'bevel_angle_limit', text="Angle")

            col.prop(self, 'bevel_profile', text="Profile", slider=True)

            col.prop(self, 'bevel_use_clamp_overlap',text="Clamp Overlap")
        # Mirror
        if self.modifier_type == 'MIRROR':
            col.use_property_split = True
            self.use_manual_type(self.use_manual,col)

            row = col.row()
            row = col.row(align=True, heading="Axis")

            row.prop(self, 'mirror_use_x', text="X", toggle=True)
            row.prop(self, 'mirror_use_y', text="Y", toggle=True)
            row.prop(self, 'mirror_use_z', text="Z", toggle=True)

            col.prop(self, 'mirror_use_clip', text="Use Clipping", toggle=True)

            col.prop(self, 'mirror_offset_u', text="Offset U", slider=True)
            col.prop(self, 'mirror_offset_v', text="Offset V", slider=True)
        # Solidify
        if self.modifier_type == 'SOLIDIFY':
            col.use_property_split = True
            self.use_manual_type(self.use_manual,col)

            col.prop(self, 'solidify_thickness')
            col.prop(self, 'solidify_offset', slider=True)
            col.prop(self, 'solidify_use_even_offset')
            col.prop(self, 'solidify_use_rim')
            if self.solidify_use_rim:
                col.prop(self, 'solidify_use_rim_only')

            ...
        # Shrinkwrap
        if self.modifier_type == 'SHRINKWRAP':
            self.use_manual_type(self.use_manual,col)

            col.use_property_split = True

            col.prop(self, 'shrinkwarp_wrap_method')
            if self.shrinkwarp_wrap_method == 'PROJECT':
                col.prop(self, 'shrinkwarp_use_negative_direction')
            col.prop(self, 'shrinkwarp_offset')
        # Array
        if self.modifier_type == 'ARRAY':
            col.use_property_split = True

            self.use_manual_type(self.use_manual,col)

            row = col.row()
            row.prop(self, 'array_along_single_axis', text="Along Single Axis")
            if self.array_along_single_axis:
                row = col.row()
                row.prop(self, 'array_set_axis', text="Axis", expand=True)
            else:
                col.prop(self, 'array_relative_offset_displace', text="Relative Offset")
            ...

            row = col.row(heading="Object Offset")
            row.prop(self, 'array_use_object_offset', text="Use Object Offset", toggle=True)
        # Triangulate
        if self.modifier_type == 'TRIANGULATE':
            col.use_property_split = True
            self.use_manual_type(self.use_manual,col)

            col.prop(self, 'triangulate_keep_custom_normals', text="Keep Custom Normals")
            col.prop(self, 'triangulate_min_vertices', text="Min Vertices")

        # Not Draw
        if self.modifier_type == 'WELD' or self.modifier_type == 'WEIGHTED_NORMAL':
            col.use_property_split = True

            self.use_manual_type(self.use_manual,col)

            col.label(text="Done!")

    def invoke(self, context: Context, event):
        wm = context.window_manager
        # return wm.invoke_props_popup(self, event)
        if self.use_manual:
            return wm.invoke_props_dialog(self)
        else:
            return self.execute(context)
    def use_manual_type(self, is_true: bool, layout)-> None:
        if is_true:
            layout.prop(self, 'modifier_type', text="Modifier Type")

class F_OT_ClearAllModifier(Operator):
    """Clear All Modifiers"""
    bl_idname = "object.f_clear_all_modifier"
    bl_label = "Clear All Modifiers"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        active_object = bpy.context.active_object
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            context.view_layer.objects.active = obj
            for mod in obj.modifiers:
                bpy.ops.object.modifier_remove(modifier=mod.name)
        # set shade flat
        bpy.ops.object.shade_flat()

        self.Log(f"{len(selected_objects)} Objects Cleared; Modifiers Total:{len(obj.modifiers)}")
        return {'FINISHED'}

class F_OT_RemoveModifier(Operator):
    bl_idname = "object.f_remove_modifier"
    bl_label = "Batch Remove Target Modifier"
    bl_option = {'REGISTER', 'UNDO'}
    
    use_input_key: bpy.props.BoolProperty(name="Input Key", default=False) # type: ignore
    modifier_key: props.get_modifier_enum() # type: ignore
    input_modifier_name: bpy.props.StringProperty(name="Modifier Name", default="") # type: ignore
    

    def execute(self, context):
        C = context
        modifier_key = self.modifier_key.title()
        ignore_list=[]
        
        for obj in C.selected_objects:
            if modifier_key in obj.modifiers.keys():
                P(f"{modifier_key} in {obj.name}")
                modifier = C.object.modifiers.get(modifier_key)
                C.object.modifiers.remove(modifier)

            else:
                ignore_list.append(obj.name)
                continue
        
        if len(ignore_list) == 0:
            self.Log("Sucess")
        else:
            self.Warning(f"{len(ignore_list)} objects not have modifier >>{modifier_key}<<")
            P(33, f"{ignore_list}")
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.use_property_split = True

        col.prop(self, "use_input_key", text="Custom Input")
        if self.use_input_key:
            col.prop(self, "input_modifier_name", text="Modifier Name")
        else:
            col.prop(self, "modifier_key", text="Modifier")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

_cls=[
    F_OT_AddModifier,
    F_OT_ClearAllModifier,
    F_OT_RemoveModifier,
]