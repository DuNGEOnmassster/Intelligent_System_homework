import numpy as np
from dataclasses import dataclass

@dataclass
class number_Node:
    map: list # now map
    h: int  # price already paid
    g: int  # differ bewteen target
    pre_map: list # pre map

