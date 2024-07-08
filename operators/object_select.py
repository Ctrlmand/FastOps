from typing import Set
import bpy
import re
from bpy.types import Context
from typing import Union
from ..utility.debug import P, Log
from ..utility.base_class import Operator

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

class F_OT_SelectObjectByName(Operator):
    """Select Same Prefix Objects"""
    bl_idname = "object.f_select_same_prefix_objects"
    bl_label = "Select Same Prefix Objects"
    bl_options = {'REGISTER', 'UNDO'}
    # select method
    def GetObjSetByName(self, context: Context, type: str):
        """Find the object have same feature in their name; return a object set"""
        # global value
        name_regular_compile = re.compile(r'(?P<prefix>[A-Za-z_]+)(?P<index>\d+)(?P<suffix>_[\w.]+)')
        objects = context.selected_objects
        count=0
        select_list=[]
        # make sure is objects
        if not objects:
            self.Error("No Objects Selected")
            return {'CANCELLED'}
        # make sure is right value
        if type not in {'prefix', 'suffix', 'both'}:
            self.Error("Invalid Type")
            return {'CANCELLED'}
        # 1.is 'prefix' or 'suffix'
        if not type  == 'both':
            # 2.traversal in selected objects
            for obj in objects:
                # 3.get name part
                name_tmp = name_regular_compile.search(obj.name)
                # make sure name is right
                if not name_tmp:
                    self.Error("Illegal Object Name Format")
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
                    self.Error("Illegal Object Name Format")
                    return {'CANCELLED'}                # 3.select object by name part
                target_prefix = name_tmp.group('prefix')
                target_suffix = name_tmp.group('suffix')
                self.Log(f"{target_prefix} {target_suffix}")
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
        obj_list = self.GetObjSetByName(context, select_by)
        if obj_list == {'CANCELLED'}:
            return {'CANCELLED'}
        # select!!!
        self.Log(f"{obj_list}")
        for obj in obj_list:
            obj.select_set(True)
        self.Log(f"selected {len(obj_list)} objects")
        return {'FINISHED'}
    
class F_OT_SelectObjectByMaterial(Operator):
    """Select Object By Material"""
    bl_idname = 'object.f_select_object_by_material'
    bl_label = "Select Object By Material"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: bpy.props.StringProperty(name= "Material Name", default="")# type:ignore
    
    def execute(self, context: Context ):
        obj_data = bpy.data.objects
        count=0
        last_obj=None

        bpy.ops.object.select_all(action='DESELECT')

        for obj in obj_data:
            mat_index = obj.material_slots.find(self.material_name)
            if mat_index == -1:
                Log(f"{obj.name} Not In View Layer")
                continue
            else:
                Log(f"{obj.name}:Material Exist")
                last_obj=obj
                if context.view_layer.objects.get(obj.name) != None:
                    Log(f"{obj.name} In View Layer")
                    obj.select_set(True)
                    count+=1
                ...
        context.view_layer.objects.active = last_obj

        # report
        if count >0:
            self.Log(f"{count} Selected")
        else:
            self.Warning(f"No Object Selected")
        return {'FINISHED'}

    def invoke(self, context, event):

        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    def draw(self, context):
        layout = self.layout

        layout.prop_search(self, "material_name", bpy.data, "materials")
        ...

class F_OT_SelectByModifier(bpy.types.Operator):
    """Select Object By Modifier"""
    bl_idname = 'object.f_select_object_by_modifier'
    bl_label = "Select Object By Modifier"
    bl_options = {'REGISTER', 'UNDO'}
    
    modifier_type: bpy.props.EnumProperty( # type: ignore
        name = "Modifier Type",
        description = "Modifier Type Enum",
        items=(
            ('DATA_TRANSFER','Data_Transfer', ''),
            ('MESH_CACHE','Mesh_Cache', ''),
            ('MESH_SEQUENCE_CACHE','Mesh_Sequence_Cache', ''),
            ('NORMAL_EDIT','Normal_Edit', ''),
            ('WEIGHTED_NORMAL','Weighted_Normal', ''),
            ('UV_PROJECT','Uv_Project', ''),
            ('UV_WARP','Uv_Warp', ''),
            ('VERTEX_WEIGHT_EDIT','Vertex_Weight_Edit', ''),
            ('VERTEX_WEIGHT_MIX','Vertex_Weight_Mix', ''),
            ('VERTEX_WEIGHT_PROXIMITY','Vertex_Weight_Proximity', ''),
            ('ARRAY','Array', ''),
            ('BEVEL','Bevel', ''),
            ('BOOLEAN','Boolean', ''),
            ('BUILD','Build', ''),
            ('DECIMATE','Decimate', ''),
            ('EDGE_SPLIT','Edge_Split', ''),
            ('NODES','Nodes', ''),
            ('MASK','Mask', ''),
            ('MIRROR','Mirror', ''),
            ('MULTIRES','Multires', ''),
            ('REMESH','Remesh', ''),
            ('SCREW','Screw', ''),
            ('SKIN','Skin', ''),
            ('SOLIDIFY','Solidify', ''),
            ('SUBSURF','Subsurf', ''),
            ('TRIANGULATE','Triangulate', ''),
            ('VOLUME_TO_MESH','Volume_To_Mesh', ''),
            ('WELD','Weld', ''),
            ('WIREFRAME','Wireframe', ''),
            ('ARMATURE','Armature', ''),
            ('CAST','Cast', ''),
            ('CURVE','Curve', ''),
            ('DISPLACE','Displace', ''),
            ('HOOK','Hook', ''),
            ('LAPLACIANDEFORM','Laplaciandeform', ''),
            ('LATTICE','Lattice', ''),
            ('MESH_DEFORM','Mesh_Deform', ''),
            ('SHRINKWRAP','Shrinkwrap', ''),
            ('SIMPLE_DEFORM','Simple_Deform', ''),
            ('SMOOTH','Smooth', ''),
            ('CORRECTIVE_SMOOTH','Corrective_Smooth', ''),
            ('LAPLACIANSMOOTH','Laplaciansmooth', ''),
            ('SURFACE_DEFORM','Surface_Deform', ''),
            ('WARP','Warp', ''),
            ('WAVE','Wave', ''),
            ('CLOTH','Cloth', ''),
            ('COLLISION','Collision', ''),
            ('DYNAMIC_PAINT','Dynamic_Paint', ''),
            ('EXPLODE','Explode', ''),
            ('FLUID','Fluid', ''),
            ('OCEAN','Ocean', ''),
            ('PARTICLE_INSTANCE','Particle_Instance', ''),
            ('PARTICLE_SYSTEM','Particle_System', ''),
            ('SOFT_BODY','Soft_Body',''),
        ),
        default= 'MIRROR',
    )
    
    def execute(self, context: Context):
        # alias
        selected_obj = context.selected_objects
        viewlayer_obj = context.view_layer.objects

        # selected_obj mount
        if len(selected_obj) == 0:
            self.select_by_modifier(modifier = self.modifier_type, ineration_obj = viewlayer_obj, is_enum = True)

        elif len(selected_obj) == 1:
            self.select_by_modifier(modifier = context.object.modifiers.keys(), ineration_obj = viewlayer_obj, is_enum = False)

        elif len(selected_obj) > 1:
            self.select_by_modifier(modifier = context.object.modifiers.keys(), ineration_obj = selected_obj, is_enum = False)
        
        # for obj in ineration_obj:
        #     if not ((obj.type == 'MESH') and (self.modifier_type in obj.modifiers.keys())):
        #         obj.select_set(False)

        return {"FINISHED"}
    

    # @classmethod
    def select_by_modifier(self, modifier: Union[list, bpy.types.EnumProperty], ineration_obj: bpy.types.bpy_prop_collection, is_enum: bool) -> None:
        resault_list=[]

        # list
        if type(modifier) == list:
            tmp_list=[]
            for string in modifier:
               tmp_list.append(str.title(string))
            modifier = tmp_list

            self.find_key_in_list(modifier, ineration_obj, resault_list, is_enum)
        # str
        else:
            modifier = str.title(modifier)

            self.find_key_in_list(modifier, ineration_obj, resault_list, is_enum)

        # reselect obj
        bpy.ops.object.select_all(action='DESELECT')
        for obj in resault_list:
            bpy.data.objects[obj].select_set(True)
        self.Log(f"{len(resault_list)} Objects Selected")

        # Debug
        P(94, f"Selected List:")
        P(93, f"{resault_list}")

    @classmethod
    def find_key_in_list(self, modifier: Union[list, str], ineration_obj: bpy.types.bpy_prop_collection, resault_list: list, is_enum: bool = False):
        if is_enum:
            for obj in ineration_obj:
                # P(37, f"modifier: {modifier}")
                if (obj.type == 'MESH') and (modifier in obj.modifiers.keys()):
                    # P(37, obj.name)
                    resault_list.append(obj.name)
        else:
            for obj in ineration_obj:
                # P(37, f"modifier: {modifier}")
                if (obj.type == 'MESH') and (modifier == obj.modifiers.keys()):
                    # P(37, obj.name)
                    resault_list.append(obj.name)

_cls=[
    F_OT_SelectObjectByName,
    F_OT_SelectObjectByMaterial,
    F_OT_SelectByModifier,
]