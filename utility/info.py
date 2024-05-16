import bpy
# Print

# RGYBPCD
def P(num: int = 37, text: str = "") -> None:
    print(f"\033[{num}m{text}\033[0m")