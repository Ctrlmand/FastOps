from bpy import utils
from .debug import PrintColored, LogRow

# Register A List Of Class
def Register(label: str, class_list: list) -> None:
    separator_color = 96
    text_col = 32
    width:int = 40

    # label
    LogRow(colorCode=separator_color, info=f" >> {label} << ", width=width, separator="-",separator_col=separator_color, side= "-")
    for cls in class_list:
        # print element
        LogRow(colorCode=text_col, info=f"{cls.__name__}", width=width, separator="",separator_col=separator_color, side= "|", left=True)
        utils.register_class(cls)
    # end
    LogRow(colorCode=separator_color, info=f"", width=width, separator="-",separator_col=separator_color, side= "-")
    return None

# Unregist A List Of Class
def Unregister(label: str, class_list: list, width:int = 40) -> None:
    PrintColored(35,f" >> {label} << ")
    for cls in class_list:
        # print element
        # print(f"\033[31m{cls.__name__}\033[0m")
        PrintColored(31, f"{cls.__name__}")
        utils.unregister_class(cls)
    return None
