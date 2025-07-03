import bpy
from .base_class import Operator
from pathlib import Path


class FileExport:
    @staticmethod
    def ExportFBX(self: Operator, folder_path: str, file_name: str):

        Path(folder_path).mkdir(parents = True, exist_ok =True)

        target_file_path = f'{folder_path}\\{file_name}.fbx'

        bpy.ops.export_scene.fbx(
            filepath= target_file_path,
            check_existing=True, 
            filter_glob='*.fbx',
            use_selection=False,
            use_visible=True,
            use_active_collection=False, collection='',
            global_scale=1.0,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_UNITS', # (enum in ['FBX_SCALE_NONE', 'FBX_SCALE_UNITS', 'FBX_SCALE_CUSTOM', 'FBX_SCALE_ALL'], (optional)) 
            use_space_transform=True,
            bake_space_transform=False,
            object_types={'ARMATURE', 'EMPTY', 'MESH', 'OTHER'}, # {'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'}
            use_mesh_modifiers=True,
            use_mesh_modifiers_render=True,
            mesh_smooth_type='FACE', # (enum in ['OFF', 'FACE', 'EDGE'], (optional))
            colors_type='SRGB',
            prioritize_active_color=False,
            use_subsurf=False,
            use_mesh_edges=False,
            use_tspace=False,
            use_triangles=False,
            use_custom_props=False,
            add_leaf_bones=True,
            primary_bone_axis='Y',
            secondary_bone_axis='X',
            use_armature_deform_only=False,
            armature_nodetype='NULL',
            bake_anim=True,
            bake_anim_use_all_bones=True,
            bake_anim_use_nla_strips=True,
            bake_anim_use_all_actions=True,
            bake_anim_force_startend_keying=True,
            bake_anim_step=1.0,
            bake_anim_simplify_factor=1.0,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=True,
            axis_forward='Y',
            axis_up='Z'
        )
        
        self.Log("Export Finished")
            