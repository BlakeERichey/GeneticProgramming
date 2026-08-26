import logging
import numpy as np
from collections import deque

class BaseIndividual:

    uuid = 1
    
    def __init__(self, genome, max_age=None):
        self.age = 0
        self.uuid = type(self).uuid
        type(self).uuid += 1
        self.parents = set()   #uuids
        self.offspring = set() #uuids
        self.living = True
        self.max_age = max_age
        
    def birthday(self,):
        self.age += 1
        self.living = self.age < self.max_age if self.max_age is not None else True

        if not self.living:
            logging.debug(f'{self} Lifespan of {type(self).max_age} Expired.')
    
    def num_offspring(self):
        """
        Returns number of offspring needed this generation to maintain a stable population.
        """
        p = 1/(type(self).max_age)
        return np.random.poisson(p, 1)[0]
    
    def is_related(self, individual, max_depth=3):
        relatives = self.relatives(max_depth)
        
        return individual in relatives

    def relatives(self, max_depth=3):
        bfs = BreadthFirstSearch(forward='offspring', reverse='parents')
        ancestors = bfs.search_reverse(self, max_depth=max_depth)
        
        relatives = set(ancestors)
        for ancestor in ancestors:
            descendents = bfs.search_forward(ancestor, max_depth=max_depth)
            relatives.update(descendents)
        
        return relatives

class BreadthFirstSearch:

    def __init__(self, forward='connected', reverse='connected'):
        """
            Forward: String containing attribute to look for of passed in nodes that indicated direction
            Reverse: String containing attribute to look for of passed in nodes that indicated direction
        """
        self.visited = set()
        self.queued = deque()
        self._forward = forward
        self._reverse = reverse
    
    def search_forward(self, node, max_depth=None):
        return self.search(node, [self._forward], max_depth)
    
    def search_reverse(self, node, max_depth=None):
        return self.search(node, [self._reverse], max_depth)

    def search(self, node, attr=None, max_depth=None):
        self.visited = set()
        self.queued = deque()
        self.queued.append(node)
        if attr is None:
            attr = set([self._reverse, self._forward])
        visited = self._search(attr, 0, max_depth)
        return visited
    
    def _search(self, attributes, depth, max_depth):
        visited = []
        if len(self.queued) and (max_depth is None or max_depth is not None and depth < max_depth):
            visit = [self.queued.popleft() for i in range(len(self.queued))]
            for node in visit:
                if node not in self.visited:
                    self.visited.add(node)
                    for attr in attributes:
                        n = getattr(node, attr, None)
                        if n is not None:  #end of sequence not yet reached

                            try: 
                                iterator = iter(n) #attr is list?
                            except TypeError:
                                iterator = [n] #or instance?

                            
                            for n in iterator:
                                if n not in self.visited:
                                    self.queued.append(n)

            visited = self._search(attributes, depth+1, max_depth)
            visit.extend(visited)
            visited = visit
        
        return visited


class Individual:
    def __init__(self, genotype, max_age):
        self.genotype = genotype
        self.max_age = max_age
    
    def create_individual(self, genome=None):
        return BaseIndividual(
            genome if genome is not None else self.genotype.random(),
            self.max_age
        )

class Population:
    def __init__(self, genotype, max_age):
        self.individuals = []
        self.individual_cls = Individual(genotype, max_age)

    def create_population(self, n):
        self.individuals = [
            self.individual_cls.create_individual()
            for _ in range(n)
        ]