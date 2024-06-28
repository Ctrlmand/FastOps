# modifiers.py

from bpy.props import EnumProperty, StringProperty

def get_modifier_enum():
    return EnumProperty(
        name="Modifier Type",
        description="Modifier Type",
        items=[
            ('MIRROR', 'Mirror', ''),
            ('SOLIDIFY', 'Solidify', ''),
            ('BEVEL', 'Bevel', ''),
            ('WEIGHTED_NORMAL', 'Weighted Normal', ''),
            ('ARRAY', 'Array', ''),
            ('WELD', 'Weld', ''),
            ('SHRINKWRAP', 'Shrinkwrap', '')
        ],
        default='MIRROR'
    )
