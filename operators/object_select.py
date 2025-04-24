from typing import Set
import bpy
import re
from bpy.types import Context
from typing import Union
from ..utility.debug import P, InfoOut
from ..utility.base_class import Operator
from ..utility.varis import *


class F_OT_SelectObjectByName(Operator):
    """Select Same Prefix Objects"""
    bl_idname = "object.f_select_same_prefix_objects"
    bl_label = "Select Same Prefix Objects"
    bl_options = {'REGISTER', 'UNDO'}

    select_method: bpy.props.EnumProperty( # type: ignore
        name="Select Method",
        items=[
            (PREF, "Prefix", ''),
            (SUFF, "Suffix", ''),
        ],
        default='prefix'
    )


    def MatchName(self, name: str):
        """"match"""
        compile = re.compile(r'(?P<prefix>[\w]+)(?P<separator>[\s_.])(?P<suffix>[a-zA-Z0-9]+)')
        return compile.match(name)

    # select method
    def GetListBySelectedName(self, context: Context, method: str):
        """Find the object have same feature in their name; return a object set"""
# -----------------------------------------------
        selected_objs = context.selected_objects
        data_objs = bpy.data.objects
        resault_list=[]

# -----------------------------------------------

        # make sure is objects
        if not selected_objs:
            self.Error("No Objects Selected")
            return {'CANCELLED'}
        # make sure is right value
        if method not in [PREF, SUFF]:

            self.Error(f"Invalid Type, type is{method}")
            return {'CANCELLED'}


        if method == PREF:
            target_name = str()
            for obj in selected_objs:
                match = self.MatchName(obj.name)
                # part

                part_prefix = match.group(PREF)
                part_suffix = match.group(SUFF)

                # low or high
                if part_suffix == LOW:
                    target_name = part_prefix + '_' + HIGH
                elif part_suffix == HIGH:
                    target_name = part_prefix + '_' + LOW
                resault_list.append(target_name)
            ...
        elif method == SUFF:
            suffix_list = []
            # get all suffix
            for obj in selected_objs:
                
                match = self.MatchName(obj.name)
                part_suffix = match.group(SUFF)
                suffix_list.append('_' + part_suffix)
            # find in data
            for obj in data_objs:
                # check obj name endswith suffix in list
                for suff in suffix_list:
                    if obj.name.endswith(suff):
                        resault_list.append(obj.name)
                        break
            ...
        # Finally
        return set(resault_list)
    def execute(self, context):
        # select method
        select_method = self.select_method

        obj_list = self.GetListBySelectedName(context, select_method)

        # check
        if obj_list == {'CANCELLED'}:
            return {'CANCELLED'}
        # debug
        InfoOut(f"{obj_list}")

        # select!!!
        for name in obj_list:
            bpy.data.objects[name].select_set(True)
        self.Log(f"selected {len(obj_list)} objects")
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout

        layout.prop(self, "select_method")
        ...

    def invoke(self, context, event):
        wm = context.window_manager
        return self.execute(context)
        ...

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
                InfoOut(f"{obj.name} Not In View Layer")
                continue
            else:
                InfoOut(f"{obj.name}:Material Exist")
                last_obj=obj
                if context.view_layer.objects.get(obj.name) != None:
                    InfoOut(f"{obj.name} In View Layer")
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