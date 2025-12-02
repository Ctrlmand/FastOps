from typing import Any, Set
import bpy
from bpy.types import Context
from ..function.classes import Operator
from ..function.debug import PrintInfo, PrintLabel, PrintTitle

class F_OT_SwitchColorSpace(Operator):
    """Switch Textures Color Space"""
    bl_idname = "node.f_switch_color_space"
    bl_label = "Switch Color Space"
    bl_options = {'REGISTER', 'UNDO'}

    # enum
    colorspace: bpy.props.EnumProperty(
        name = "Image Color Space",
        description = "Image Color Space",
        default = 'Non-Color',
        items =(
            ('Non-Color', 'Non-Color', ''),
            ('sRGB', 'sRGB', ''),
            ('ACES 2.0 sRGB', 'ACES 2.0 sRGB', ''),

        )
    ) # type: ignore

    def execute(self, context: Context):
        sucess_count=0
        fail_count=0
        for node in context.selected_nodes:
            # self.Log(f"{node.image}")
            if node.type == "TEX_IMAGE":
                node.image.colorspace_settings.name = self.colorspace
                sucess_count+=1
                ...
            else:
                fail_count+=1
        if sucess_count>0:
            self.Log(f"{sucess_count} nodes sucessfully changed, {fail_count} nodes failed")
        else:
            self.Warning(f"no texture nodes found")
        return {'FINISHED'}

class F_OT_ReportSelectedTextureNodeName(Operator):
    """Report the name of the selected texture node"""
    bl_idname = "node.f_report_selected_texture_node_name"
    bl_label = "Report Selected Texture Node Name"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context: Context):
        success=0
        ignore=0
        # traverse selected nodes and report the name 
        for node in context.selected_nodes:
            if node.type == 'TEX_IMAGE':
                self.Log(f"{node.image.name}")
                self.Log(f"{node.image.filepath}")
                self.Log(f"{node.type}")
                success+=1
            else:
                ignore+=1
        self.Log(f"success:{success},ignore:{ignore}")
        return{'FINISHED'}

class F_OT_ImageNodeMergeRGBAndAlpha(Operator):
    """Image Node Merge RGB And Alpha"""
    bl_idname = "node.f_image_node_merge_rgb_and_alpha"
    bl_label = "Image Node Merge RGB And Alpha"
    bl_options = {'REGISTER', 'UNDO'}
    # method of merge rgb and a
    def merge_rgb_and_a(self, rgb_image: bpy.types.Image, a_image: bpy.types.Image):
        """Merge RGB And Alpha"""
        # get pixels
        rgb_pixels = rgb_image.pixels
        a_pixels = a_image.pixels
        # switch type
        rgb_pixels = list(rgb_pixels)
        a_pixels = list(a_pixels)

        # append info to list
        # 首先对 zip() 结果进行迭代，然后对每个四元组内的元素（r, g, b, a）进行二次迭代
        resault_pixels = [r for tup in zip(rgb_pixels[0::4], rgb_pixels[1::4], rgb_pixels[2::4], a_pixels[0::4]) for r in tup]
        # resault_pixels = [r for r in rgb_pixels[::4] + [0,0] * (len(resault_pixels) // 4 * 3)]

        # return resault
        return resault_pixels
    def execute(self, context: Context):
        # get rgb and a image
        image_list=[]
        for node in context.selected_nodes:
            image_list.append(node.image.name)
        image_list.remove(context.active_node.image.name)
        rgb_name = image_list[0]
        a_name = context.active_node.image.name

        # get image pixel
        rgb_image = bpy.data.images[rgb_name]
        a_image = bpy.data.images[a_name]
        # check size
        if rgb_image.size[0] != a_image.size[0] or rgb_image.size[1] != a_image.size[1]:
            self.Error(f"{rgb_name} and {a_name} size not equal")
            return {'CANCELLED'}
        # check final image exist in database
        if not f"{rgb_name}_WithAlpha" in bpy.data.images:
            final_img = bpy.data.images.new(f"{rgb_name}_WithAlpha", rgb_image.size[0], rgb_image.size[1])
        else:
            final_img = bpy.data.images[f"{rgb_name}_WithAlpha"]
        # merge and store
        final_img.pixels = self.merge_rgb_and_a(rgb_image, a_image)

        # image_texture_node = bpy.ops.node.add_node(type="ShaderNodeTexImage")
        nodes = context.active_object.active_material.node_tree.nodes
        links = context.active_object.active_material.node_tree.links
        # create node
        final_node = nodes.new(type='ShaderNodeTexImage')
        final_node.location = (0,0)
        final_node.image = final_img

        return {'FINISHED'}

class F_OT_FindMaterialByTextureNode(Operator):
    """FindMaterialByTextureNode"""
    bl_idname = "object.f_find_material_by_texture"
    bl_label = "Find Material By Texture"
    bl_options = {'REGISTER', 'UNDO'}

    image_name: bpy.props.StringProperty(name="Image Name", default="") # type: ignore
    show_hide: bpy.props.BoolProperty(name="Show Hide", default=False) # type: ignore

    def execute(self, conxtex):
        # debug
        PrintTitle("Find Material By Texture Node")

        IMAGE_TEXTURE = 'Image Texture'
        TEX_IMAGE = 'TEX_IMAGE'

        mat_temp=[]
        obj_temp=[]

        # traverse data to find material that has target texture node 
        for material in bpy.data.materials:
            PrintTitle(f"\tMaterial: {material.name}")

            # material has no node tree
            if not material.use_nodes:
                continue

            node_tree = material.node_tree

            # if there has texture node in node tree
            if IMAGE_TEXTURE in node_tree.nodes.keys():

                # traverse texture node in material
                for node in node_tree.nodes.values():
                    # if node's type same as target type
                    if node.type == TEX_IMAGE and node.image != None:
                        PrintLabel(f"\t\t{node.image.name}")
                        # if node's name same as target name
                        if node.image.name == self.image_name:
                            mat_temp.append(material.name)
                            PrintInfo(f"\t\t\tHas Target Texture")
                            break
                    else:
                        continue
                        ...
                    ...
                ...
            # if there has texture node
            else:
                continue
        
        mat_temp = set(mat_temp)
        # traverse data to find objects has target material
        for object in bpy.data.objects:
            if object.type == 'MESH':
                material_slots = object.material_slots.keys()
                # if objects's material slots has target material
                if set(material_slots).intersection(mat_temp):
                    obj_temp.append(object.name)
                    ...
                else:
                    continue
            # when object not a mesh
            else:
                continue
        
        obj_temp = set(obj_temp)

        # traverse data to find objects in set
        for name in obj_temp:
            obj = bpy.data.objects[name]
            
            bpy.ops.object.select_all(action='DESELECT')

            # if show hide
            if obj.hide_get():
                obj.hide_set(not self.show_hide)
            # if select
            if not obj.hide_get():
                obj.select_set(True)

        # self.Log(f"{len(obj_temp)} objects has target texture")
        self.Log(f"Done!")
        
        return {"FINISHED"}

    def draw(self, context: Context | Any):
        layout = self.layout
        layout.prop_search(self, "image_name", bpy.data, "images")
        layout.prop(self, "show_hide")
        ...

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

_cls=[
    F_OT_SwitchColorSpace,
    F_OT_ReportSelectedTextureNodeName,
    F_OT_ImageNodeMergeRGBAndAlpha,
    F_OT_FindMaterialByTextureNode,
]