from bpy import utils
from ..utility.debug import P, P_row
# Register A List Of Class
def Register(label: str, class_list: list) -> None:
    separator_col = 96
    text_col = 32
    width:int = 40

    # label
    P_row(col_info=separator_col, info=f" >> {label} << ", width=width, separator="-",separator_col=separator_col, side= "-")
    for cls in class_list:
        # print element
        P_row(col_info=text_col, info=f"{cls.__name__}", width=width, separator="",separator_col=separator_col, side= "|", left=True)
        utils.register_class(cls)
    # end
    P_row(col_info=separator_col, info=f"", width=width, separator="-",separator_col=separator_col, side= "-")
    return None
# Unregist A List Of Class
def Unregister(label: str, class_list: list, width:int = 40) -> None:
    P(35,f" >> {label} << ")
    for cls in class_list:
        # print element
        # print(f"\033[31m{cls.__name__}\033[0m")
        P(31, f"{cls.__name__}")
        utils.unregister_class(cls)
    return None
