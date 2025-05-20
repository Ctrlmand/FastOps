import bpy
import re

from .global_variable import *
from ..utility.debug import InfoOut, LabelOut, TitleOut

def match_obj(list: list, type: str) -> list:
    """Match Objects By Type In List"""
    # valid type
    type_list = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'CURVES', 'POINTCLOUD', 'VOLUME', 'GPENCIL', 'GREASEPENCIL',]
    # assert
    assert type in type_list
    
    # body
    empty_cout=0
    resault=[]
    for obj in list:
            # 1.if obj not mesh
            if obj.type != type:
                empty_cout+=1
                continue
            resault.append(obj)
    return resault


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
        LabelOut("MatchObjectByPrefix: matching failed")
        return None

    # get matched info
    part_prefix = match.group(PREF)
    part_suffix = match.group(SUFF)

    # low or high
    if part_suffix == LOW:
        target_name = part_prefix + '_' + HIGH
    elif part_suffix == HIGH:
        target_name = part_prefix + '_' + LOW

    # if there has no target object in data
    if not target_name in bpy.data.objects.keys():
        LabelOut(f'No target object: {target_name}')
        return None

    target_name

    return bpy.data.objects[target_name]
    ...
