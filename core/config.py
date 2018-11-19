# coding=utf-8

class Config:
    INPUT_DIR = "input"



    STOCK_ID_NAME_MAP_SHA = "input/common/stock_id_name_map/sha"
    STOCK_ID_NAME_MAP_SZ = "input/common/stock_id_name_map/sz"
    STOCK_ID_NAME_MAP_OPEN = "input/common/stock_id_name_map/open"

    CURRENT_HOLDED_PATH = "input/holded"

    STOCKS_PATH = "input/stocks"

    SELECTED_FILE = "selected"
    SELECTED_PATH = "input/selected/selected"

    OPTION_HOLDED = 1
    OPTION_SELECTED = 2

    #持续增长考察年份数
    CONTINUE_GROW_YEARS = 6
    #持续增长容许最多亏损
    ALLOW_MAX_LOSS = -0.10

    def __init__(self):
        pass
