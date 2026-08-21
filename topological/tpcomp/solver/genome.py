from tpcomp.solver.gene import Structural
from tpcomp.solver.chromosome import ObservationChromosome, ActionChromosome

class Genome:
    def __init__(self, n_obs, n_act):
        self.actions    = {i: ActionChromosome() for i in range(n_act)}
        self.observations = {i: ObservationChromosome() for i in range(n_obs)}
        self.sequence = {
            'actions':    self.actions,
            'observations': self.observations,
        }

    # def __str__(self):
    #     action_lines = ["Actions:", "{"]
    #     for chrom in self.actions.values():
    #         print(chrom)
    #         print(chrom.sequence)
    #         for loci, gene_values in chrom.sequence.items():
    #             if type(gene_values) is Structural:
    #                 action_lines.append(['    ', loci, str(gene_values)])
    #             else:
    #                 action_lines.append(['    ', loci, map(str, gene_values)])

    #     print(action_lines)    
    #     return '\n'.join(action_lines)#'\n'.join(map('\n'.join, [line for line in action_lines]))
        # 'Genome:\n' + str(self.sequence) + '\n'
        