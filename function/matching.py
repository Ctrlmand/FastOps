import bpy
import re

from ..function.debug import PrintLabel

def MatchObjectByPrefix(obj):
    """Match objects by prefix"""
    # return object when match successed
    # return null when failed
#---------------------------------------------------
    target_name = str()

#---------------------------------------------------
    # match
    compile = re.compile(r'(?P<prefix>[\w]+)(?P<separator>[\s_.])(?P<suffix>[a-zA-Z0-9]+)')
    match = compile.match(obj.name)

    # if match failed
    if not match:
        PrintLabel("MatchObjectByPrefix: matching failed")
        return None

    # get matched info
    part_prefix = match.group('prefix')
    part_suffix = match.group('suffix')

    # low or high
    if part_suffix == 'low':
        target_name = part_prefix + '_' + 'high'
    elif part_suffix == 'high':
        target_name = part_prefix + '_' + 'low'

    # if there has no target object in data
    if not target_name in bpy.data.objects.keys():
        PrintLabel(f'No target object: {target_name}')
        return None

    target_name

    return bpy.data.objects[target_name]
    ...
