from tpcomp.solver.gene import Structural, Position, \
    Decay, StimulusAmp, \
    VelocityAmp, Sensitivity, \
    FieldOfViewCenter1, FieldOfViewWidth1, \
    FieldOfViewCenter2, FieldOfViewWidth2

class ObservationChromosome:
    def __init__(self, sequence=None):        
            if sequence is None:
                sequence = {
                    0: Structural(value=False)
                }
                sequence.update(
                    {
                        i+1: gene_type.random() 
                        for i, gene_type in enumerate((
                            Position(),
                            Decay(),
                            StimulusAmp(),
                            VelocityAmp(),
                            Sensitivity(),
                        ))
                    }
                )
            self.sequence = sequence

class ActionChromosome:
    def __init__(self, sequence=None):        
        if sequence is None:
            sequence = {
                0: Structural(value=True)
            }
            sequence.update(
                {
                    i+1: gene_type.random() 
                    for i, gene_type in enumerate((
                        Position(),
                        Decay(),
                        StimulusAmp(),
                        VelocityAmp(),
                        Sensitivity(),
                        FieldOfViewCenter1(),
                        FieldOfViewWidth1(),
                        FieldOfViewCenter2(),
                        FieldOfViewWidth2()
                    ))
                }
            )
        self.sequence = sequence