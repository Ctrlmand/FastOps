
def CommonColor(col:int =37, info:str="")->str:
    return f"\033[{col}m{info}\033[0m"

# col: int
# info: any
def PrintColored(col: int = 37, info: any = None) -> None:

    print(CommonColor(col,info))

def LogRow(colorCode:int = 37, info:any = None, width:int = 40, separator:str='', separator_col:int = 37, side:str='|', right:bool = False, left:bool = False, center:bool=False) -> None:
    # align mode
    align=""
    if right:
        align = '>'
    elif left:
        align = '<'
    elif center:
        align = '^'
    else:
        align = '^'
    
    print(CommonColor(separator_col, side)+f"\033[{colorCode}m{info:{separator}{align}{width}}\033[0m"+CommonColor(separator_col, side))

def PrintInfo(info:any) -> None:
    PrintColored(col=96, info=info)

def PrintLabel(info:any) -> None:
    PrintColored(col=93, info=info)

def PrintTitle(info:any) -> None:
    PrintColored(col=91, info=info)