from enum import IntEnum

# values of the possible methods to get an initial solution
class MethodType(IntEnum):
    NORTH_WEST_METHOD = 1
    VOGEL_METHOD = 2
    RUSSELL_METHOD = 3
    LEAST_COST_CELL_METHOD = 4
    LEAST_COST_ROW_METHOD = 5
    LEAST_COST_COLUMN_METHOD = 6
