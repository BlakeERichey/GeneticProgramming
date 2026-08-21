from tpcomp.solver.gene import Position, \
    Decay, StimulusAmp, \
    VelocityAmp, Sensitivity, \
    FieldOfViewCenter, FieldOfViewWidth, \
    Decision

class Chromosome:
    sequence = {}
    def __repr__(self):
        msg = f'{type(self).__name__}('
        msg += '\n  '.join(f'{key}={value}' for key, value in self.sequence.items())
        msg += '\n)'
        return msg
            

class ObservationChromosome(Chromosome):
    def __init__(self, sequence=None):        
            if sequence is None:
                sequence = {}
                sequence.update(
                    {
                        i: gene_type.random() 
                        for i, gene_type in enumerate((
                            Position(),
                            Decay(),
                            StimulusAmp(),
                            VelocityAmp(),
                            Sensitivity(),
                            #FOV arity=0
                        ))
                    }
                )
            self.sequence = sequence

class ActionChromosome(Chromosome):
    def __init__(self, sequence=None):        
        if sequence is None:
            sequence = {}
            sequence.update(
                {
                    i: gene_type.random() 
                    for i, gene_type in enumerate((
                        Position(),
                        Decay(),
                        StimulusAmp(),
                        VelocityAmp(),
                        Sensitivity(),
                        FieldOfViewCenter(), 
                        FieldOfViewWidth(),

                        # should be resolved via arity... deferred for now
                        FieldOfViewCenter(),
                        FieldOfViewWidth()
                    ))
                }
            )
        self.sequence = sequence


class LutChromosome(Chromosome):
    def __init__(self, sequence=None):        
            if sequence is None:
                sequence = {}
                sequence.update(
                    {
                        i: gene_type.random() 
                        for i, gene_type in enumerate((
                            Decision(),
                            # should be resolved via arity... deferred for now; arity=5
                            Decision(),
                            Decision(),
                            Decision(),
                            Decision(),
                        ))
                    }
                )
            self.sequence = sequence