
def strCol(col:int =37, info:str="")->str:
    return f"\033[{col}m{info}\033[0m"

# col: int
# info: any
def P(col: int = 37, info: any = None) -> None:

    print(strCol(col,info))

def P_row(col_info:int = 37, info:any = None, width:int = 40, separator:str='', separator_col:int = 37, side:str='|', right:bool = False, left:bool = False, center:bool=False) -> None:
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
    
    print(strCol(separator_col, side)+f"\033[{col_info}m{info:{separator}{align}{width}}\033[0m"+strCol(separator_col, side))

def InfoOut(info:any) -> None:
    P(col=96, info=info)

def LabelOut(info:any) -> None:
    P(col=93, info=info)

def TitleOut(info:any) -> None:
    P(col=91, info=info)