# modifiers.py

from bpy.props import EnumProperty

def get_modifier_enum() -> EnumProperty:
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
            ('SHRINKWRAP', 'Shrinkwrap', ''),
            ('TRIANGULATE', 'Triangulate', ''),

        ],
        default='MIRROR'
    )
