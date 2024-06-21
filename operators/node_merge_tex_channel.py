from typing import Any
import bpy
from bpy.types import Context 
from ..utility.base_class import Operator

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
_cls=[
    F_OT_ReportSelectedTextureNodeName,
    F_OT_ImageNodeMergeRGBAndAlpha,
]