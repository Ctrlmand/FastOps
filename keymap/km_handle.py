import bpy
from .. import operators, ui
from ..utility.debug import P_row

# keymap list
addon_km=[]
# Register
def register():
    # keymaps
    wm = bpy.context.window_manager
    # >> Switch Image Display Channel <<
    km_image_editor = wm.keyconfigs.addon.keymaps.new(name='Image', space_type='IMAGE_EDITOR')

    kmi_image_editor_channel_red = km_image_editor.keymap_items.new(operators.Image_switch_channel.F_OT_ImageChannelSet.bl_idname, 'R', 'PRESS', ctrl=False, shift=False)
    kmi_image_editor_channel_red.properties.channel = 'RED'

    kmi_image_editor_channel_green = km_image_editor.keymap_items.new(operators.Image_switch_channel.F_OT_ImageChannelSet.bl_idname, 'G', 'PRESS', ctrl=False, shift=False)
    kmi_image_editor_channel_green.properties.channel = 'GREEN'
    
    kmi_image_editor_channel_blue = km_image_editor.keymap_items.new(operators.Image_switch_channel.F_OT_ImageChannelSet.bl_idname, 'B', 'PRESS', ctrl=False, shift=False)
    kmi_image_editor_channel_blue.properties.channel = 'BLUE'

    kmi_image_editor_channel_alpha = km_image_editor.keymap_items.new(operators.Image_switch_channel.F_OT_ImageChannelSet.bl_idname, 'A', 'PRESS', ctrl=False, shift=False)
    kmi_image_editor_channel_alpha.properties.channel = 'ALPHA'

    kmi_image_editor_channel_color = km_image_editor.keymap_items.new(operators.Image_switch_channel.F_OT_ImageChannelSet.bl_idname, 'C', 'PRESS', ctrl=False, shift=False)
    kmi_image_editor_channel_color.properties.channel = 'COLOR'

    kmi_image_editor_channel_color_alpha = km_image_editor.keymap_items.new(operators.Image_switch_channel.F_OT_ImageChannelSet.bl_idname, 'C', 'PRESS', ctrl=True, shift=False)
    kmi_image_editor_channel_color_alpha.properties.channel = 'COLOR_ALPHA'

    ## append to km
    image_editor_kmi_list=[
        kmi_image_editor_channel_red,
        kmi_image_editor_channel_green,
        kmi_image_editor_channel_blue,
        kmi_image_editor_channel_alpha,
        kmi_image_editor_channel_color,
        kmi_image_editor_channel_color_alpha
    ]
    addon_km.append((km_image_editor, image_editor_kmi_list))

    # >> Node Option KM << 
    km_node_editor = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')

    kmi_node_editor_call_menu_pie = km_node_editor.keymap_items.new('wm.call_menu_pie', 'F', 'PRESS', ctrl=False, shift=False, alt=False)
    kmi_node_editor_call_menu_pie.properties.name = ui.pie_NodeEditor.FASTOPS_MT_NodeOptionPieMenu.bl_idname

    ## append to km
    node_editor_kmi_list=[
        kmi_node_editor_call_menu_pie
    ]
    addon_km.append((km_node_editor, node_editor_kmi_list))

    ...
    # >> Object Modifier & Object Alternate KM <<
    km_object_3dview = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi_object_3dview_call_modifier_pie = km_object_3dview.keymap_items.new('wm.call_menu_pie', 'F', 'PRESS', ctrl=False, shift=False, alt=False)
    kmi_object_3dview_call_modifier_pie.properties.name = ui.pie_View3D.VIEW3D_MT_ModifierPieMenu.bl_idname

    kmi_object_3dview_call_material_pie = km_object_3dview.keymap_items.new('wm.call_menu_pie', 'F', 'PRESS', ctrl=True, shift=False, alt=False)
    kmi_object_3dview_call_material_pie.properties.name = ui.pie_View3D.VIEW3D_MT_AlternatePieMenu.bl_idname
    ## append to km
    object_3dview_kmi_list=[
        kmi_object_3dview_call_modifier_pie,
        kmi_object_3dview_call_material_pie
    ]
    addon_km.append((km_object_3dview, object_3dview_kmi_list))
  

    # >> debug << 
    P_row(col_info= 96, info = ">> KM REGISTED <<", separator='-', separator_col=96, side="-")
    # traverse km and kmi
    for km, kmi_list in addon_km:
        P_row(col_info= 36, info = f"> {km.name} <", separator='', separator_col=96, side="|")
        for kmi in kmi_list:
            P_row(col_info= 32, info = f"{kmi.name}", separator='', separator_col=96, side="|", left=True)
    # end
    P_row(col_info=96, info=f"", separator="-",separator_col=96, side= "-")
# Unregister
def unregister():
    for km, kmi_list in addon_km:
        for kmi in kmi_list:
            km.keymap_items.remove(kmi)
    addon_km.clear()
    ...
