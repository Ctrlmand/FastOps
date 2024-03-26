from bpy import utils
# Register A List Of Class
def register(label: str, class_list: list) -> None:
    print(f"\033[33m >> {label} << \033[0m")
    for cls in class_list:
        # print element
        print(f"\033[32m{cls.__name__}\033[0m")
        utils.register_class(cls)
    return None
# Unregist A List Of Class
def unregister(label: str, class_list: list) -> None:
    print(f"\033[33m >> {label} << \033[0m")
    for cls in class_list:
        # print element
        print(f"\033[31m{cls.__name__}\033[0m")
        utils.unregister_class(cls)
    return None
