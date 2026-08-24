import logging
import numpy as np
class BaseColony:
    
    ######################## CASE DEFINED ########################
    _lineage_cls = NotImplementedError('Must Set Default Lineage for Colony')
    ##############################################################

    def __init__(self, lineages=10, default_lineage_size=10, diversity=None, max_age=None):
        self._lineage = self._lineage_cls
        self.lineages = []
        self.default_lineage_size = default_lineage_size
        self.diversity = diversity
        
        assert max_age is not None, "Must set maximum age for individuals"
        self._lineage_cls._individual_cls.max_age = max_age

        if lineages is not None:
            for _ in range(lineages):
                self.introduce_family(self.default_lineage_size)
    
    def __repr__(self,):
        msg = f'{type(self)}\n_lineage: {self._lineage}\nlineages: List[{len(self.lineages)}\ndefault_lineage_size: {self.default_lineage_size}\ndiversity: {self.diversity}]'
        return msg
    
    def introduce_family(self, initial_pop, species=None):
        self.lineages.append(self._lineage(initial_pop, species=species))
    
    @property
    def pop_size(self,):
        return len(self.get_living())

    def get_living(self, by_species=False):
        """
        Returns all living invididuals
        by_species: If byspecies is True, will return dictionary with keys being the speciess
            If byspecies is False, will return set containing individuals
        """
        living = None
        if by_species:
            individuals_by_species = {}
            for family in self.lineages:
                for species, individuals in family.get_living(by_species=True).items():
                    current = individuals_by_species.setdefault(species, set())
                    current.update(individuals)
        
            living = individuals_by_species

        else:  
            individuals = set()
            for family in self.lineages:
                individuals.update(family.get_living())
            
            living = individuals
        
        return living
    
    @property
    def all_individuals(self,):
        individuals = set()
        for family in self.lineages:
            individuals.update(family.all_individuals)
        
        return individuals
    
    def _get_individual(self, uuid):
        for individual in self.all_individuals:
            if individual.uuid == uuid:
                break
            
            if individual.uuid != uuid:
                raise KeyError(f'I#{uuid} not found.')

        return individual

    def update_lineages(self):
        """
        Age every member and update their current living status
        """
        i_perished = 0
        f_perished = 0
        remaining = []
        
        for individual in self.get_living():
            individual.birthday()
        
            if not individual.living:
                i_perished+=1

        for i, family in enumerate(self.lineages):  
            living_individuals = family.get_living()
            if len(living_individuals):
                remaining.append(family)
                forgotten = family.all_individuals
                for individual in living_individuals:
                    forgotten = forgotten - individual.relatives()
            
                #forgotten = no living individual that is closely related
                for individual in forgotten:
                    family._remove_individual(individual)
            else:
                f_perished+=1
        
        if i_perished:
            print(f'Individuals perished: {i_perished}')
        if f_perished:
            print(f'Lineages perished: {f_perished}/{len(self.lineages)}')
        self.lineages = remaining

    def _selection(self,):
        """
        Returns all individuals that are slated to reproduce this generation
        by following a poisson distribution of replacing the population within 
        each individuals lifespan
        """
        all_influences = []
        for individual in self.get_living():
            all_influences.append(individual.influence)
        
        mean_influence = np.array(all_influences).mean()
        logging.debug(f'Mean Influence: {mean_influence}')
        
        for species, individuals in self.get_living(by_species=True).items():
            eligible = {}
            
            for i, individual in enumerate(individuals):
                num_offspring = individual.num_offspring(mean_influence)
                
                if num_offspring > 0:
                    eligible.update({individual: num_offspring})
            
            eligible = {
                k: v 
                for k, v in 
                sorted(
                eligible.items(), 
                key=lambda item: item[0].influence, #higher influence = more candidates
                reverse=True
                )
            }

            logging.debug(f'Eligible: {eligible}')
            
            yield eligible, species

    def procreate(self):
        num_new = 0
        
        for mating_pool, species in self._selection():
            avg_candidates = 0
            if len(mating_pool):
                offsprings, avg_candidates = self._reproduce(mating_pool)
                logging.debug(f'New BBs: {len(offsprings)}')
                num_new += len(offsprings)
                logging.info(f'Average Candidates Available for {species}: {avg_candidates}')

            #Occuring when no mating pool due to lack of pioneers
            if self.diversity is not None:
                if avg_candidates < self.diversity:
                    delta = int(np.ceil(self.diversity - avg_candidates))
                    num_new += delta
                    for i in range(delta):
                        self.introduce_family(1, species)
            
            logging.debug(f'\n\nNew Individuals Created: {num_new}')
        
        return num_new
    
    def _reproduce(self, mating_pool):
        num_candidates = []
        
        logging.debug(f'Mating Pool: {mating_pool}')
        new_offspring = set()
        if len(mating_pool) > 0:
            for parentA, num_offspring in mating_pool.items():
                logging.debug(f'Parent {parentA} eligible for {num_offspring}')
                if num_offspring:
                    candidates = set()
                    
                    relatives = parentA.relatives()
                    for individual in mating_pool:
                        if not (individual in relatives) and mating_pool[individual] > 0:
                            candidates.add(individual)
                    
                    if not len(candidates):
                        logging.debug(f'Eligible, but no candidates available')
                        #   im = parentA.similar()
                        #   candidates.add(im)
                    
                    num_candidates.append(len(candidates))
                    logging.debug(f'Candidates: {len(candidates)}')
                    
                    while num_offspring > 0 and len(candidates):
                        #individuals ranked by influence, therefore higher influence => more candidates
                        parentB = np.random.choice(list(candidates), 1, False)[0]
                        logging.debug(f'Breeding with {parentB}')

                        max_offspring = min(mating_pool.get(parentB, 1), num_offspring)
                        for i in range(max_offspring):
                            offspring = type(parentA).breed(parentA, parentB)
                            new_offspring.add(offspring)
                            logging.info(f'Offspring: {offspring} | From: {parentA} / {parentB} | Influence: {offspring.influence}')
                            
                            mating_pool[parentA] -= 1
                            if parentB in mating_pool: #if not immigrant
                                mating_pool[parentB] -= 1
                        
                        num_offspring -= max_offspring
                        if parentB not in mating_pool or mating_pool[parentB] == 0:
                            candidates.remove(parentB)
                
        
        return new_offspring, np.array(num_candidates).mean()