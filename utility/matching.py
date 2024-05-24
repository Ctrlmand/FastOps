import bpy

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