import numpy as np


###INFO about the dweller
class Dweller:
    def __init__(self,name,stats):
        self.name = name
        if not isinstance(stats,list) or len(stats)!= 1:
            raise Exception("error")
        else:
            self.stats = stats

#INFO about the move
class move():
    pass


