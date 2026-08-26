import numpy as np
class PositiveWitness:
    def __init__(self,):
        self.best_fitness = 1
        self._proceed    = False
        self._permission = True

    @property
    def permission(self):
        return self._permission

    @property
    def proceed(self):
        return self._proceed

    def review(self, results):
        best = np.max(results)
        if best > self.best_fitness:
            self.best_fitness = best
            self._proceed = True # if meets minimum, transfer to next bracket
        else:
            self._proceed = False