import imp
import numpy as np
from dataclasses import dataclass

@dataclass
class number_Node:
    map: np.array() # now map
    h: int  # price already paid
    g: int  # differ bewteen target
    pre_map: np.array() # pre map

